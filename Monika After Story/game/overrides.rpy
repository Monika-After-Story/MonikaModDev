## This file is for overriding specific declarations from DDLC
## Use this if you want to change a few variables, but don't want
## to replace entire script files that are otherwise fine.

## Normal overrides
## These overrides happen after any of the normal init blocks in scripts.
## Use these to change variables on screens, effects, and the like.
init 10 python:
    pass

## Early overrides
## These overrides happen before the normal init blocks in scripts.
## Use this in the rare event that you need to overwrite some variable
## before it's called in another init block.
## You likely won't use this.
init -10 python:
    pass

## Super early overrides
## You'll need a block like this for creator defined screen language
## Don't use this unless you know you need it
python early in mas_overrides:
    import ast
    from renpy.python import py_eval_bytecode
    from renpy.pyanalysis import ccache

    def slblock_prepare(self, analysis):


        for i in self.children:
            i.prepare(analysis)
            self.constant = min(self.constant, i.constant)

        # Compile the keywords.

        keyword_values = { }
        keyword_keys = [ ]
        keyword_exprs = [ ]

        for k, expr in self.keyword:

            node = ccache.ast_eval(expr)

            const = analysis.is_constant(node)

            if const == renpy.sl2.slast.GLOBAL_CONST:
                keyword_values[k] = py_eval_bytecode(renpy.sl2.slast.compile_expr(self.location, node))
            else:
                keyword_keys.append(ast.Str(s=k))
                keyword_exprs.append(node) # Will be compiled as part of ast.Dict below.

            self.constant = min(self.constant, const)

        if keyword_values:
            self.keyword_values = keyword_values
        else:
            self.keyword_values = None

        if keyword_keys:
            node = ast.Dict(keys=keyword_keys, values=keyword_exprs)
            ast.copy_location(node, keyword_exprs[0])
            self.keyword_exprs = renpy.sl2.slast.compile_expr(self.location, node)
        else:
            self.keyword_exprs = None

        self.has_keyword = bool(self.keyword)
        self.keyword_children = [ ]

        if self.atl_transform is not None:
            self.has_keyword = True

            self.atl_transform.mark_constant()
            const = self.atl_transform.constant
            self.constant = min(self.constant, const)

        was_last_keyword = False
        for i in self.children:
            if i.has_keyword:

                #Disable this exception because it's stupid
                #if was_last_keyword:
                #    raise Exception("Properties are not allowed here.")

                self.keyword_children.append(i)
                self.has_keyword = True

            if i.last_keyword:
                self.last_keyword = True
                was_last_keyword = True
                if not renpy.config.developer:
                    break

    renpy.sl2.slast.SLBlock.prepare = slblock_prepare
