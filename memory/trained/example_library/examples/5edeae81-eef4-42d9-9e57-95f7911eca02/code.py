# TASK: write the word HELLO, starting from the top-left corner of the workspace

workspace = Workspace()
start_position = parse_location_description('top-left corner')
all_blocks = get_objects()
write_word_with_blocks('HELLO', all_blocks, start_position)