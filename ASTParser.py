import ast
import re
from GraphNode import GraphNode
from ASTUtils import get_node_value


class ASTParser(ast.NodeVisitor):
    def __init__(self, func_list):
        super(ASTParser, self).__init__()
        self.df_graph = []
        self.scope=""
        self.obj_list = {}
        self.func_list = func_list
        self.imports = {}

    def add_lib_objects(self, lib_name):
        try:
            lib = __import__(lib_name)
            pattern = re.compile('__\\w+__')
            for member in dir(lib):
                if pattern.match(member) is None:
                    if member not in self.imports.keys():
                        self.imports[member] = [lib_name + '.' + member]
                    else:
                        self.imports[member].append(lib_name + '.' + member)
        except:
            pass

    def get_source_list(self, source_fn_list, suffix="", result=None):
        if result is None:
            result = []
        if len(source_fn_list) == 0:
            if len(result) == 0:
                return [suffix[1:]]
            return result
        elif ".".join(source_fn_list) in self.imports.keys():
            key = ".".join(source_fn_list)
            for value in self.imports[key]:
                result.append(value + suffix)
            return result
        else:
            return self.get_source_list(source_fn_list[:-1],
                                        "." + source_fn_list[-1]
                                        + suffix, result)

    def clear_obj_list(self,scope):
        if scope in self.obj_list.keys():
            for obj in self.obj_list[scope]:
                self.df_graph.append(
                    GraphNode(obj, '--dies--', ''))
            del self.obj_list[scope]
        self.scope="module"

    def visit_Module(self, node):
        scope="module"
        self.obj_list[scope]=[]
        self.scope=scope
        self.generic_visit(node)
        self.clear_obj_list(scope)

    def visit_FunctionDef(self,node):
        scope='_'.join(['function',node.name])
        self.obj_list[scope]=[]
        self.scope=scope
        self.generic_visit(node)
        self.clear_obj_list(scope)

    def visit_ImportFrom(self, node):
		lib = node.module
		for name in node.names:
			if name.asname is not None:
				alias = name.asname
				if lib is None:
					pass
				elif alias not in self.imports.keys():
					self.imports[alias] = [lib + '.' + name.name]
				else:
					if '.'.join([lib,name.name]) not in self.imports[alias]:
						self.imports[alias].append('.'.join([lib,name.name]))
			else:
				module = name.name
				if lib is None:
					pass
				elif '*' == module:
					self.add_lib_objects(lib)
				elif module not in self.imports.keys():
					self.imports[module] = [lib + '.' + module]
				else:
					if '.'.join([lib,module]) not in self.imports[module]:
						self.imports[module].append('.'.join([lib,module]))
		return self.generic_visit(node)


    def visit_Import(self, node):
        for name in node.names:
            if name.asname is not None:
                self.imports[name.name] = [name.asname]
        return self.generic_visit(node)

    def visit_Assign(self, node):
        object_list=self.obj_list[self.scope]
        for target in node.targets:
            tgt=[target]
            if isinstance(target, ast.Tuple):
                tgt=target.elts
            t_value=[]
            for t in tgt:
                t_value.append(".".join(get_node_value(t)))
            target=','.join(t_value)
            if self.scope == "module":
                target="glob:"+target

            if target not in object_list:
                for t in t_value:
                    if t in object_list:
                        self.df_graph.append(
                            GraphNode(t, '--dies--', ''))
                        self.obj_list[self.scope].remove(t)

            else:
                self.df_graph.append(
                    GraphNode(target, '--dies--', ''))
                self.obj_list[self.scope].remove(target)

            if isinstance(node.value, ast.Call):
                src_func_name = get_node_value(node.value.func)
                fn_name = ".".join(src_func_name)
                if fn_name not in self.func_list:
                    srclist = self.get_source_list(src_func_name)
                    for func_name in srclist:
                        self.df_graph.append(
                            GraphNode(func_name,'--becomes--', target))
                    self.obj_list[self.scope].append(target)
        return self.generic_visit(node)

    def visit_Attribute(self, node):
        attr_func_name = get_node_value(node)
        glob_attr_func_name = attr_func_name
        glob_attr_func_name[0]="glob:"+glob_attr_func_name[0]
        if len(attr_func_name) != 0:
            for i in range(1,len(attr_func_name)):
                obj_list=[obj for values in self.obj_list.values() for obj in values]
                if ".".join(attr_func_name[:i]) in obj_list:
                    self.df_graph.append(
                        GraphNode(".".join(attr_func_name[:-1]), '--calls--', attr_func_name[-1]))
                    break
                elif ".".join(attr_func_name[:i]) in obj_list:
                    self.df_graph.append(
                        GraphNode(".".join(glob_attr_func_name[:-1]), '--calls--', glob_attr_func_name[-1]))
                    break

        return self.generic_visit(node)

    def visit_Subscript(self, node):
        """dummy function to prevent visiting the nodes if subscripts are present"""

    def visit_For(self,node):
         """dummy function to prevent visiting the nodes if for loops are present"""

    def visit_With(self, node):
        with_expr=".".join(get_node_value(node.context_expr))
        scope="_".join(['with',with_expr])
        self.scope=scope
        self.obj_list[self.scope]=[]
        if isinstance(node.context_expr, ast.Call):
            target = ".".join(get_node_value(node.optional_vars))
            if len(target) != 0:
                self.df_graph.append(
                    GraphNode(with_expr,'--becomes--', target))
                self.obj_list[self.scope].append(target)
        self.generic_visit(node)
        self.clear_obj_list(scope)