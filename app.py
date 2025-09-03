import sys
from utils.config import CONFIG
if '--mode' in sys.argv:
    i = sys.argv.index('--mode') + 1
    if i < len(sys.argv):
        mode = sys.argv[i]
    else:
        mode = 'cli'
else:
    mode = 'cli'
if mode == 'web':
    from interfaces.web import run_app
    run_app()
else:
    from interfaces.cli import main
    main()