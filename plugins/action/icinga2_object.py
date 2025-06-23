# pylint: disable=consider-using-f-string,super-with-arguments
import re

from ansible.errors import AnsibleError
from ansible.plugins.action import ActionBase
from ansible.utils.vars import merge_hash
from ansible_collections.netways.icinga.plugins.module_utils.parse import Icinga2Parser


class ActionModule(ActionBase):

    def run(self, tmp=None, task_vars=None):

        result = super(ActionModule, self).run(tmp, task_vars)

        args = dict()
        args = self._task.args.copy()
        args = merge_hash(args.pop('args', {}), args)
        object_type = args.pop('type', None)

        if object_type not in task_vars['icinga2_object_types']:
            raise AnsibleError('unknown Icinga object type: %s' % object_type)

        #
        # distribute to object type as module (name: icinga2_type)
        #
        obj = dict()
        obj = self._execute_module(
            module_name='icinga2_'+object_type.lower(),
            module_args=args,
            task_vars=task_vars,
            tmp=tmp
        )

        if 'failed' in obj:
            raise AnsibleError('Call to module failed: %s' % obj['msg'])
        if 'skipped' in obj and obj['skipped']:
            raise AnsibleError('Call to module was skipped: %s' % obj['msg'])

        #
        # file path handling for assemble
        #
        path = task_vars['icinga2_fragments_path'] + '/' + obj['file'] + '/'
        file_fragment = path + obj['order'] + '_' + object_type.lower() + '-' + obj['name']

        if obj['state'] != 'absent':
            file_args = dict()
            file_args['state'] = 'directory'
            file_args['path'] = path
            file_module = self._execute_module(
                module_name='file',
                module_args=file_args,
                task_vars=task_vars,
                tmp=tmp
            )
            result = merge_hash(result, file_module)

            varlist = list()  # list of variables from 'apply for'

            #
            # quoting of object name?
            #
            if obj['name'] not in task_vars['icinga2_combined_constants']:
                object_name = '"' + obj['name'] + '"'
            else:
                object_name = obj['name']

            #
            # apply rule?
            #
            if 'apply' in obj and obj['apply'] and not obj['args']['assign']:
                raise AnsibleError('Apply rule %s is missing the assign rule.' % obj['name'])
            if 'apply' in obj and obj['apply']:
                object_content = 'apply ' + object_type
                if 'apply_target' in obj and obj['apply_target']:
                    object_content += ' ' + object_name + ' to ' + obj['apply_target']
                elif 'apply_for' in obj and obj['apply_for']:
                    object_content += ' for (' + obj['apply_for'] + ') '
                    r = re.search(r'^(.+)\s+in\s+', obj['apply_for'])
                    if r:
                        tmp = r.group(1).strip()
                        r = re.search(r'^(.+)=>(.+)$', tmp)
                        if r:
                            varlist.extend([r.group(1).strip(), r.group(2).strip()])
                        else:
                            varlist.append(tmp)
                else:
                    object_content += ' ' + object_name
            #
            # template?
            #
            elif 'template' in obj and obj['template']:
                object_content = 'template ' + object_type + ' ' + object_name
            #
            # object
            #
            else:
                object_content = 'object ' + object_type + ' ' + object_name
            object_content += ' {\n'

            #
            # imports?
            #
            if 'imports' in obj:
                for item in obj['imports']:
                    object_content += '  import "' + str(item) + '"\n'
                object_content += '\n'

            #
            # parser
            #
            object_content += Icinga2Parser().parse(
                obj['args'],
                list(task_vars['icinga2_combined_constants'].keys()) + task_vars['icinga2_reserved'] + varlist + list(obj['args'].keys()),
                2
            ) + '}\n'
            copy_action = self._task.copy()
            copy_action.args = dict()
            copy_action.args['dest'] = file_fragment
            copy_action.args['content'] = object_content

            copy_action = self._shared_loader_obj.action_loader.get(
                'copy',
                task=copy_action,
                connection=self._connection,
                play_context=self._play_context,
                loader=self._loader,
                templar=self._templar,
                shared_loader_obj=self._shared_loader_obj
                )

            result = merge_hash(result, copy_action.run(task_vars=task_vars))
        else:
            # remove file if does not belong to a feature
            if 'features-available' not in path:
                file_args = dict()
                file_args['state'] = 'absent'
                file_args['path'] = file_fragment
                file_module = self._execute_module(
                    module_name='file',
                    module_args=file_args,
                    task_vars=task_vars,
                    tmp=tmp
                )
                result = merge_hash(result, file_module)
            result['dest'] = file_fragment

        return result
