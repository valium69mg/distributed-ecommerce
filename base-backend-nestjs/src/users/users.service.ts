import { HttpException, HttpStatus, Injectable } from "@nestjs/common";
import { CreateUserDTO } from "./dto/create-user.dto";
import { AppDataSource } from "src/data-source";
import * as bcrypt from "bcrypt";
import { v4 as uuidv4 } from "uuid";
import GetUserDTO from "./dto/get-user.dto";
import { User } from "./users.entity";
import UpdateUserDTO from "./dto/update-user.dto";

const SALT_ROUNDS = 10;

@Injectable()
export class UserService {
  constructor() {}

  async userExistsByEmail(email: string): Promise<boolean> {
    const result: unknown[] = await AppDataSource.query(
      `SELECT 1 FROM users WHERE email = ? LIMIT 1`,
      [email],
    );
    return result.length > 0;
  }

  async create(createUserDTO: CreateUserDTO): Promise<boolean> {
    const { email, password } = createUserDTO;

    const hashedPassword = await bcrypt.hash(password, SALT_ROUNDS);

    try {
      const existByEmail = await this.userExistsByEmail(email);
      if (existByEmail) {
        throw new HttpException(
          "User already registered with email: " + email,
          HttpStatus.BAD_REQUEST,
        );
      }
      const role = await AppDataSource.query(
        `SELECT role_id FROM roles WHERE name = ?`,
        [createUserDTO.role],
      );

      if (role.length === 0) {
        throw new HttpException(
          "User already registered with email: " + email,
          HttpStatus.BAD_REQUEST,
        );
      }

      const role_id = role[0].role_id;
      const uuid = uuidv4();

      await AppDataSource.query(
        `INSERT INTO users (user_id, email, password, role_id) VALUES (?, ?, ?, ?)`,
        [uuid, email, hashedPassword, role_id],
      );

      return true;
    } catch (error) {
      throw new HttpException(
        "Could not create user: " + error,
        HttpStatus.INTERNAL_SERVER_ERROR,
      );
    }
  }

  async update(updateUserDto: UpdateUserDTO): Promise<boolean> {
    const result = await AppDataSource.query(
      `
        UPDATE users SET email = ? WHERE user_id = ?
      `,
      [updateUserDto.email, updateUserDto.userId],
    );

    if (result.affectedRows > 0) {
      return true;
    }
    return false;
  }

  async validateUser(
    email: string,
    plainPassword: string,
  ): Promise<User | null> {
    const result = await AppDataSource.query(
      `SELECT * FROM users WHERE email = ?`,
      [email],
    );

    if (result.length === 0) return null;

    const user = result[0];
    const isMatch = await bcrypt.compare(plainPassword, user.password);
    return isMatch ? user : null;
  }

  async getUserById(userId: string): Promise<GetUserDTO> {
    const result = await AppDataSource.query(
      `
        SELECT * FROM users WHERE user_id = ?
      `,
      [userId],
    );
    if (result.length > 0) {
      return { userId: result[0].user_id, email: result[0].email };
    }
    throw new HttpException("User not found", HttpStatus.NOT_FOUND);
  }

  async getUsers(): Promise<Array<GetUserDTO>> {
    const results = await AppDataSource.query(`
        SELECT * FROM users
      `);
    if (results.length > 0) {
      return results.map((r) => {
        return { userId: r.user_id, email: r.email };
      });
    }
    return [];
  }

  async deleteUserById(userId: string): Promise<boolean> {
    const result = await AppDataSource.query(
      `
        DELETE FROM users WHERE user_id = ?
      `,
      [userId],
    );
    console.log(result);
    if (result.affectedRows > 0) {
      return true;
    }
    throw new HttpException(
      "Could not delete user",
      HttpStatus.INTERNAL_SERVER_ERROR,
    );
  }
}
