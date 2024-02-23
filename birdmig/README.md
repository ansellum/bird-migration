# Usage

## To start the Flask Backend:
- cd into /birdmig/backend
- enter ```flask run``` in your terminal

## To start the React Frontend:

- cd into /birdmig
- enter ```npm start``` in your terminal

## To run the Docker image:
- Ensure that flask is running in the background. (Refer to the Flask section above)
- Open Docker
- Build the docker file: docker build -t bird_migration .
- Docker run -d -p destination_port:source_destination --name bird_migration bird_migration
- Open http://localhost:destination_port TODO: this actually doesn't work. React is working in the background, but for whatever reason connecting to local host doesn't do anything. Fix this!