import { Body, Controller, Get, Logger, Param, Post, RawBodyRequest, Req } from '@nestjs/common';
import { AppService } from './app.service';
import { Car } from './car/car.entity';

@Controller()
export class AppController {
  constructor(private readonly appService: AppService) {}

  @Get()
  getHello(): string {
    return this.appService.getHello();
  }

  @Post()
  async create(@Req() req: RawBodyRequest<Request>): Promise<string> {
    Logger.log('POST !!!');
    Logger.log(JSON.parse(req.rawBody.toString()));

    return "sucesso";
  }
  
}
