import { MigrationInterface, QueryRunner } from "typeorm";

export class DropIsAdminFromUsers1760670048808 implements MigrationInterface {
  public async up(queryRunner: QueryRunner): Promise<void> {
    await queryRunner.query(`
      ALTER TABLE users DROP COLUMN isAdmin;
    `);
  }

  public async down(queryRunner: QueryRunner): Promise<void> {
    await queryRunner.query(`
      ALTER TABLE users ADD COLUMN isAdmin BOOLEAN DEFAULT false;
    `);
  }
}
