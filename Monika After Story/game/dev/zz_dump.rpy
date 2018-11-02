# emergency dumping file

init 3000 python:
    # outfiles
    outtext = (
        "mrt: {0}\nmerr: {1}\nmmrh: {2}\nrs: {3}\n"
    )
    basedir = config.basedir.replace("\\", "/")
    with open(basedir + "/dumps.log", "w") as dump_file:
        dump_file.write(outtext.format(
            len(monika_random_topics),
            persistent._mas_enable_random_repeats,
            persistent._mas_monika_repeated_herself,
            persistent.random_seen
        )
    )
    del outtext

