import { NestFactory } from "@nestjs/core";
import { AppModule } from "./app.module";
import { AppDataSource } from "./data-source";

async function bootstrap() {
  await AppDataSource.initialize();
  const app = await NestFactory.create(AppModule);
  await app.listen(process.env.PORT ?? 3000, "0.0.0.0", () => {
    console.log("Server running on port 3000");
  });
}
bootstrap();
