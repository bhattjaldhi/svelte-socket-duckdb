FROM node:18.18.0-alpine AS builder

WORKDIR /app

COPY package*.json .

RUN npm i -g npm
RUN npm install socket.io-client --save
RUN npm install

COPY . .

RUN npm run build

FROM node:18.8.0-alpine AS deployer

WORKDIR /app

COPY --from=builder /app/build build/
COPY --from=builder /app/package.json .
COPY --from=builder /app/node_modules node_modules/

EXPOSE 3000

ENV NODE_ENV=production

CMD [ "node", "build" ]