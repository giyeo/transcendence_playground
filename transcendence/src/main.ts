import { NestFactory } from '@nestjs/core';
import { AppModule } from './app.module';
import * as http from 'http';
import * as cors from 'cors';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);

  // Enable CORS with allowed origins
  app.use(
    cors({
      origin: 'http://localhost:8080', // Replace with your Svelte app's URL
    })
  );

  const server = http.createServer(app.getHttpAdapter().getInstance());
  const io = require('socket.io')(server);

  io.on('connection', (socket) => {
    console.log('Client connected');
    // Handle WebSocket events here
    socket.on('disconnect', () => {
      console.log('Client disconnected');
    });
  });

  server.listen(3000);
}
bootstrap();
