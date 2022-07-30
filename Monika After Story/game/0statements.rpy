python early in mas_statements:
    from collections import namedtuple

    __AugJumpParseData = namedtuple("__AugJumpParseData", ("label", "is_expression", "arg_info"))


    def __aug_jump(label, args, kwargs):
        """
        Jumps to the given label and passes the provided args and kwargs
        You're probably looking for mas_aug_jump which
            utilises Python's * and ** starred syntax

        IN:
            label - the label to jump to
            args - the positional arguments for the label
            kwargs - the named arguments forthe label
        """
        renpy.store._args = args
        renpy.store._kwargs = kwargs
        renpy.jump(label)

    def mas_aug_jump(label, *args, **kwargs):
        """
        Jumps to the given label and passes the provided args and kwargs

        IN:
            label - the label to jump to
            *args - the positional arguments for the label
            **kwargs - the named arguments forthe label
        """
        __aug_jump(label, args, kwargs)


    def __get_label(parsed_data):
        """
        Returns label from the parsed data
        NOTE: may raise exceptions

        IN:
            parsed_data - __AugJumpParseData for this statement

        OUT:
            str
        """
        label_ = parsed_data.label
        if parsed_data.is_expression:
            label_ = eval(label_)
        return label_

    def __parse_augmented_jump(lex):
        """
        Parses the aug_jump statement

        IN:
            lex - the Lexer object

        OUT:
            __AugJumpParseData
        """
        lex.expect_noblock("aug_jump")

        if lex.keyword("expression"):
            is_expression = True
            label_ = lex.require(lex.simple_expression)
            lex.keyword("pass")

        else:
            is_expression = False
            label_ = lex.require(lex.label_name)

        arg_info = renpy.parser.parse_arguments(lex)

        lex.expect_eol()
        lex.advance()

        return __AugJumpParseData(label_, is_expression, arg_info)

    def __execute_augmented_jump(parsed_data):
        """
        Executes the aug_jump statement

        IN:
            parsed_data - __AugJumpParseData for this statement
        """
        label_ = __get_label(parsed_data)

        arg_info = parsed_data.arg_info
        if arg_info:
            args, kwargs = arg_info.evaluate()
            __aug_jump(label_, args, kwargs)

        else:
            __aug_jump(label_, None, None)

    def __predict_augmented_jump(parsed_data):
        """
        Predicts the aug_jump statement

        IN:
            parsed_data - __AugJumpParseData for this statement
        """
        try:
            label_ = __get_label(parsed_data)
        except Exception:
            return

        if not renpy.has_label(label_):
            return

        return [renpy.game.script.lookup(label)]

    def __lint_augmented_jump(parsed_data):
        """
        A lint function for the aug_jump statement

        IN:
            parsed_data - __AugJumpParseData for this statement
        """
        try:
            label_ = __get_label(parsed_data)
        except Exception:
            return

        if not renpy.has_label(label_):
            raise Exception("aug_jump is being used with unknown label: '{}'", label_)


    # Define the new statement
    renpy.register_statement(
        "aug_jump",
        parse=__parse_augmented_jump,
        execute=__execute_augmented_jump,
        predict=__predict_augmented_jump,
        lint=__lint_augmented_jump
    )
    # Expose to the global namespace
    renpy.store.mas_aug_jump = mas_aug_jump
