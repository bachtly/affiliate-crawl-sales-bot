all: dependency run
dev: run

dependency:
	@echo "Setup dependencies..."
	mkdir -p log

clean:
	@echo "Clean up..."
	rm -rf log

run:
	@echo "Start app..."
	source venv/bin/activate && python3 app.py

chrome:
	@echo "Start app..."
	sudo apt update
	sudo apt install -y unzip xvfb libxi6 libgconf-2-4
	sudo apt install default-jdk

	sudo curl -sS -o - https://dl-ssl.google.com/linux/linux_signing_key.pub | sudo apt-key add
	sudo bash -c "echo 'deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main' >> /etc/apt/sources.list.d/google-chrome.list"
	sudo apt -y update
	sudo apt -y install google-chrome-stable

	google-chrome --version
	wget https://chromedriver.storage.googleapis.com/94.0.4606.61/chromedriver_linux64.zip
	unzip chromedriver_linux64.zip
	sudo mv chromedriver /usr/bin/chromedriver
	sudo chown root:root /usr/bin/chromedriver
	sudo chmod +x /usr/bin/chromedriver
	sudo rm chromedriver_linux64.zip

SHELL = /bin/bash
.DEFAULT_GOAL := all
