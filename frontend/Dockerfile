# Use Node 18 as the base image
FROM node:18

# Set the working directory inside the container
WORKDIR /app

# Copy package.json and package-lock.json, then install dependencies
COPY package.json package-lock.json ./
RUN npm install

# Copy the entire frontend code into the container
COPY . .

# Expose port 3000 for the Next.js app
EXPOSE 3000

# Command to run the Next.js app
CMD ["npm", "run", "dev"]
