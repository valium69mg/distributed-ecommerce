import { Module } from "@nestjs/common";
import { UserService } from "./users.service";
import { UserController } from "./users.controller";
import { RolesModule } from "src/roles/roles.module";

@Module({
  controllers: [UserController],
  providers: [UserService],
  exports: [UserService],
  imports: [RolesModule],
})
export class UserModule {}
