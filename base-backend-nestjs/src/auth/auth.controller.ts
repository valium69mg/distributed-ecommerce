import {
  Controller,
  Post,
  Body,
  UnauthorizedException,
  Get,
  Req,
} from "@nestjs/common";
import { JwtService } from "@nestjs/jwt";
import { UserService } from "src/users/users.service";
import type RequestWithUser from "src/users/dto/request-with-user.dto";
import { JwtAuthGuard } from "src/guards/jwt-auth.guard";
import { UseGuards } from "@nestjs/common";
import { RolesService } from "src/roles/roles.service";
import AuthCredentialsDto from "./dto/auth-credentials.dto";

@Controller("auth")
export class AuthController {
  constructor(
    private jwtService: JwtService,
    private userService: UserService,
    private rolesService: RolesService,
  ) {}

  @Post("login")
  async login(@Body() body: { email: string; password: string }) {
    const user = await this.userService.validateUser(body.email, body.password);
    if (!user) {
      throw new UnauthorizedException("Invalid credentials");
    }

    const payload = {
      userId: user.user_id,
      email: user.email,
    };

    return {
      access_token: this.jwtService.sign(payload),
    };
  }

  @Get()
  @UseGuards(JwtAuthGuard)
  async auth(@Req() req: RequestWithUser): Promise<AuthCredentialsDto> {
    const user = req.user;
    const roles: string[] = await this.rolesService.getRolesById(
      req.user.userId,
    );
    return {
      userId: user.userId,
      roles: roles,
    };
  }
}
