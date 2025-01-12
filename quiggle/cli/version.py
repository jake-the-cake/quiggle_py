## local imports
from quiggle.tools.logs.event import EventLog
from quiggle.tools.printer import print_error, print_note, colors
from quiggle.tools.reader.reader import Reader
from quiggle.vars.array import Array

# global veriables for tne function
VERSION_NUMBER = 'VERSION_NUMBER'
VERSION_PARTS = {
	'major': 0,
	'minor': 1,
	'patch': 2
}

def update_version(cli, path: str) -> None:

	# filter out non-accepted flags and options
  cli.filter_options(['minor', 'major'])
  cli.filter_flags(['n'])
  
	# initialize a reader with the file path and extra the data by line
  reader: Reader = Reader(path)
  lines:    list = reader.get_lines()
  # initialize event log
  log:  EventLog = EventLog('version.json').get_json_data()

  original_version = None

  for line in lines:
    if line.starts_with(VERSION_NUMBER, line.strip_newline_tag):
      array = Array(line.get_value('=').strip('\''), split='.', items=3)
      original_version = array.to_string('.')
      if len(cli.values) > 0:
        array = Array(cli.values[0], split='.', items=3) 
        original_version = array.to_string('.')
      elif len(cli.options) == 0:
        array.increase_numeric_value_by_index(2, 1)
      else:  
        for option in cli.options:
          values = option['values']
          index = VERSION_PARTS[option['option']]
          if len(values) == 0: values = ['+', '1']
          if len(values) == 1: values = ['='] + values
          array.edit_numeric_value_by_index(index, int(values[1]), values[0])
        if 'n' not in cli.flags:
          if not any(item.get('option') == 'minor' for item in cli.options):
            array.edit_numeric_value_by_index(1, 0, '=')
          array.edit_numeric_value_by_index(2, 0, '=')  
      new_version = array.to_string('.')
      log.add_property('version', new_version)
      line.set_data(f'{ VERSION_NUMBER } = \'{ new_version }\'', line.append_newline_tag)
    reader.updated_lines.append(line.data)
  
  def log_entry():
    log.use_log_message('notes', colors.yellow('Update notes: '))
    if len(log.entry['notes']) > 0:
      log.add_entry()
      reader.write()
      log.write()
    else:
      print_error('Update notes are required.')
      log_entry()
  if not original_version:
    print_note(f'Existing version number not found in { path }')
  else:
    print_note(f'Update to version { colors.white_on_green(new_version) } (previous: { colors.white_on_red(original_version) })')
    log_entry()