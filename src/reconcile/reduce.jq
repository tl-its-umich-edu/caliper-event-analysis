def walk(f):
  . as $in
  | if type == "object" then
      reduce keys_unsorted[] as $key
        ( {}; . + { ($key):  ($in[$key] | walk(f)) } ) | f
  elif type == "array" then map( walk(f) ) | f
  else f
  end;

walk(
  if type == "object" then with_entries(select(.value|length > 0))
  elif type == "array" then map(select(length > 0))
  else .
  end
)
