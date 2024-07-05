from ..core.utils.array import trim_array

def split_path(path):
	return trim_array(path.split('/'))

def get_filename(path: str) -> str:
	return split_path(path)[-1]