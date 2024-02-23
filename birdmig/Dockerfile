# Start an image with node base image.
# node:18 is essentially node.js to help construct the web file.
FROM node:18-alpine

# Sets the /app directory, or the CWDir.
WORKDIR /app

# Copy contents of package.json files for utility.
COPY package*.json ./
#COPY . .

# Run additional commands for startup
RUN npm install 
COPY . ./

# Begin the program
#CMD [ "npm" ]
ENTRYPOINT [ "npm",  "start" ]