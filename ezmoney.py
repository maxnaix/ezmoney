import threading
import queue
import telegramd


def main():
	threading.Thread(target=telegramd.telegram_handler, daemon=False).start()
	#while True:
	#	s = input


if __name__ == "__main__":
	main()
