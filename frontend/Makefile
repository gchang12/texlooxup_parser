APP_NAME := texlooxup_dict
.frontend:
	xfce4-terminal --working-directory=/home/eclair/Documents/coding/_web-dev/$(APP_NAME)/frontend/$(APP_NAME)/app/ &
	printf '\033]0;%s\007' "react-server";
	cd $(APP_NAME)/ && npm run dev -- --open --port 3000;
