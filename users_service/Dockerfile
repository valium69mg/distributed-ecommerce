# Stage 1: Build the app
FROM node:20-alpine AS builder

# Set working directory
WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm install

# Copy source code
COPY . .

# Build the app
RUN npm run build

# Stage 2: Run the app
FROM node:20-alpine

# Set working directory
WORKDIR /app

# Copy built files and dependencies from builder
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package.json ./

# Expose port (adjust if needed)
EXPOSE 3000

# Start the app
CMD ["node", "dist/main"]
