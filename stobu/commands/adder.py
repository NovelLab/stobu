"""Command process module for adding."""

# Official Libraries


# My Modules


__all__ = (
        'switch_command_to_add',
        )


# Main
def switch_command_to_add(cmdargs: argparse.Namespace) -> bool:
    assert cmdargs.cmd in ('a', 'add')

    is_succeeded = False

    if cmdargs.arg0 in ('c', 'chapter'):
        is_succeeded = add_new_chapter(cmdargs.arg1)
    elif cmdargs.arg0 in ('e', 'episode'):
        is_succeeded = add_new_episode(cmdargs.arg1)
    elif cmdargs.arg0 in ('s', 'scene'):
        is_succeeded = add_new_scene(cmdargs.arg1)
    elif cmdargs.arg0 in ('n', 'note'):
        is_succeeded = add_new_note(cmdargs.arg1)
    elif cmdargs.arg0 in ('p', 'person'):
        is_succeeded = add_new_person(cmdargs.arg1)
    elif cmdargs.arg0 in ('t', 'stage'):
        is_succeeded = add_new_stage(cmdargs.arg1)
    elif cmdargs.arg0 in ('i', 'item'):
        is_succeeded = add_new_item(cmdargs.arg1)
    elif cmdargs.arg0 in ('w', 'word'):
        is_succeeded = add_new_word(cmdargs.arg1)
    elif cmdargs.arg0 in ('d', 'todo'):
        is_succeeded = todom.add_todo(cmdargs.arg1)
    elif cmdargs.arg0 in ('l', 'plan'):
        is_succeeded = add_new_plan(cmdargs.arg1)
    elif cmdargs.arg0 in ('o', 'outline'):
        is_succeeded = add_new_outline(cmdargs.arg1)
    elif cmdargs.arg0 in ('v', 'event'):
        is_succeeded = add_new_event(cmdargs.arg1)
    else:
        logger.error("Unknown add command argument!: %s", cmdargs.arg0)
        return False

    if not is_succeeded:
        logger.error("...Failed command add!")
        return False

    logger.debug("...Succeeded command add.")
    return True


