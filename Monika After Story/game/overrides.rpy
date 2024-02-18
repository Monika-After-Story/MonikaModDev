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
    def verify_data_override(data, signatures, check_verifying=True):
        """
        Verify the data in a save token.

        Originally, this function is used to check against a checksum to verify the persistent should be loaded
        But because we want to allow anyone be able to migrate and transfer their data, we will just return True
        """
        return True

    renpy.savetoken.verify_data = verify_data_override
