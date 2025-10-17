import { Injectable, CanActivate, ExecutionContext } from "@nestjs/common";
import { Reflector } from "@nestjs/core";
import { Roles } from "src/decorators/roles.decorator";
import { UserService } from "src/users/users.service";
import RequestWithUser from "src/users/dto/request-with-user.dto";
import { RolesService } from "src/roles/roles.service";

@Injectable()
export class RolesGuard implements CanActivate {
  constructor(
    private reflector: Reflector,
    private readonly userService: UserService,
    private readonly rolesService: RolesService,
  ) {}

  async canActivate(context: ExecutionContext): Promise<boolean> {
    const roles = this.reflector.get(Roles, context.getHandler());
    if (!roles) {
      return true;
    }
    const request = context.switchToHttp().getRequest<RequestWithUser>();
    const user = request.user;
    const userId = user.userId;
    const userRoles = await this.rolesService.getRolesById(userId);
    return matchRoles(roles, userRoles);
  }
}

function matchRoles(requiredRoles: string[], userRoles: string[]): boolean {
  return requiredRoles.some((role) => userRoles.includes(role));
}
