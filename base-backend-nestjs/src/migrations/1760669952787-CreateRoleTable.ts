import { MigrationInterface, QueryRunner } from "typeorm";

export class CreateRoleTable1760669952787 implements MigrationInterface {
  name = "CreateRoleTable1760669952787";

  public async up(queryRunner: QueryRunner): Promise<void> {
    await queryRunner.query(
      `CREATE TABLE \`roles\` (\`role_id\` varchar(36) NOT NULL, \`name\` varchar(255) NOT NULL, \`created_at\` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP, PRIMARY KEY (\`role_id\`)) ENGINE=InnoDB`,
    );
  }

  public async down(queryRunner: QueryRunner): Promise<void> {
    await queryRunner.query(`DROP TABLE \`roles\``);
  }
}
