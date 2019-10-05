import sys

if __name__ == '__main__':
    cmd = sys.argv[1]

    if cmd == 'run':
        from app.server import run
        run()
    elif cmd == 'test':
        from tests.main import run
        run()