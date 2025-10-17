import { Injectable } from "@nestjs/common";
import { HttpException, HttpStatus } from "@nestjs/common";
import { AppDataSource } from "src/data-source";
@Injectable()
export class RolesService {
  async getRolesById(userId: string): Promise<string[]> {
    const result = await AppDataSource.query(
      `
        SELECT r.name AS role
        FROM users u
        JOIN roles r ON u.role_id = r.role_id
        WHERE u.user_id = ?
    `,
      [userId],
    );

    if (result.length === 0) {
      throw new HttpException("User not found", HttpStatus.NOT_FOUND);
    }

    return [result[0].role];
  }
}
