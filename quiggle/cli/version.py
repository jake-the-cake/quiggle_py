## local imports
from quiggle.vars.array import Array
from quiggle.tools.reader.reader import Reader

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

  for line in lines:
    if line.starts_with(VERSION_NUMBER, line.strip_newline_tag):
      array = Array(line.get_value('=').strip('\''), split='.', items=3)
      if len(cli.values) > 0:
        array = Array(cli.values[0], split='.', items=3) 
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
      line.set_data(f'{ VERSION_NUMBER } = \'{ array.to_string('.') }\'', line.append_newline_tag)
    reader.updated_lines.append(line.data)
  reader.write()