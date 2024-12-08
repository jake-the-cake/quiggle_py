## local imports
from quiggle.config import globals
from quiggle.tools.logs.presets import labellog
from quiggle.vars.array import Array
from quiggle.tools.reader import Reader, Parser


def update_version(cli, path: str) -> None:
  cli.filter_options(['minor', 'major'])
  cli.filter_flags(['n'])
  
  reader: Reader = Reader(path)
  lines:    list = reader.get_lines()
    
  updated_lines = []
  version_parts = {
    'major': 0,
    'minor': 1,
    'patch': 2
  }

  for line in lines.lines:
    line = Parser(line)
    if line.starts_with('VERSION_NUMBER'):
      line.strip_newline_tag()
      array = Array(line.get_value('=').strip('\''), split='.', items=3)
      if len(cli.values) > 0:
        array = Array(cli.values[0], split='.', items=3) 
      else:  
        for option in cli.options:
          if len(option['values']) == 0:
            option['values'] = ['+', '1']
          if len(option['values']) == 1:
            option['values'] = ['='] + option['values']
          array.values[version_parts[option['option']]] = array.change_value_by_index(version_parts[option['option']], int(option['values'][1]))[option['values'][0]]
        if 'n' not in cli.flags:
          if not any(item.get('option') == 'minor' for item in cli.options):
            array.values[1] = array.change_value_by_index(1, 0)['=']
          array.values[2] = array.change_value_by_index(2, 0)['=']
          
      line.data = 'VERSION_NUMBER = \'' + array.to_string('.') + '\''
      line.append_newline_tag()

    updated_lines.append(line.data)



    #   split_line = line.data.replace(' ', '').replace('\n', '').split('=')
    #   if len(cli.values) > 0:
    #     if len(cli.values[0].split('.')) != 3:
    #       updated_lines.append(line)
    #       print(labellog('Invalid version format.'))
    #       continue
    #     split_line[1] = '\'' + cli.values[0] + '\'\n'
    #   elif len(cli.options) > 0:
    #     for option in cli.options:
    #       version_parts = split_line[1].replace('\'', '').split('.')
    #       if option['option'] == 'minor':
    #         if len(option['values']) > 0:
    #           if option['values'][0] == '+':
    #             version_parts[1] = str(int(version_parts[1]) + int(option['values'][1]))
    #           elif option['values'][0] == '-':
    #             version_parts[1] = str(int(version_parts[1]) - int(option['values'][1]))
    #           else:
    #             version_parts[1] = option['values'][0]
    #         else:
    #           version_parts[1] = str(int(version_parts[1]) + 1)
    #         if 'n' not in cli.flags:
    #           version_parts[2] = '0'
    #       if option['option'] == 'major':
    #         version_parts[0] = str(int(version_parts[0]) + 1)
    #         if 'n' not in cli.flags:
    #           version_parts[2] = '0'
    #           version_parts[1] = '0'
    #       split_line[1] = '\'' + '.'.join(version_parts) + '\'\n'
    #   else:
    #     split_line[1] += '\n'
    #   updated_lines.append(' = '.join(split_line))
    # else: updated_lines.append(line.data)
  print(''.join(updated_lines))