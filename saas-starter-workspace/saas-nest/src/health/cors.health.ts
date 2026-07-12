import { Controller, Get, HttpCode, HttpStatus } from "@nestjs/common";

import {
  CorsService,
  CorsHealthPayload,
} from "../modules/free/security/cors/cors.service";

@Controller("api/health/module")
export class CorsHealthController {
  constructor(private readonly service: CorsService) {}

  @Get("cors")
  @HttpCode(HttpStatus.OK)
  getModuleHealth(): CorsHealthPayload {
    return this.service.getHealthPayload();
  }
}
