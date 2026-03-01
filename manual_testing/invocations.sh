./example_error.sh >out.log 2>&1 || ../appendorgheading/__init__.py --output out.org --filecontent out.log --title "example call with error"
./example_nonerror.sh >out.log 2>&1 || ../appendorgheading/__init__.py --output out.org --filecontent out.log --title "example call without error"
