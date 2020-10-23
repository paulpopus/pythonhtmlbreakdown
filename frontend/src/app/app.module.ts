import { BrowserModule } from '@angular/platform-browser';
import { CommonModule } from '@angular/common';
import { NgModule } from '@angular/core';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { ApidocComponent } from './apidoc/apidoc.component';
import { HomeComponent } from './home/home.component';
import { TagComponent } from './tag/tag.component';
import { AccordionComponent } from './accordion/accordion.component';

import { HttpClientModule } from '@angular/common/http';
import { RouteReuseStrategy } from '@angular/router';
import { CustomRouteReuseStrategy } from './routing/routeCaching';

@NgModule({
  declarations: [
    AppComponent,
    ApidocComponent,
    HomeComponent,
    TagComponent,
    AccordionComponent
  ],
  imports: [
    CommonModule,
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
  ],
  providers: [{
    provide: RouteReuseStrategy,
    useClass: CustomRouteReuseStrategy,
  }],
  bootstrap: [AppComponent]
})
export class AppModule { }
