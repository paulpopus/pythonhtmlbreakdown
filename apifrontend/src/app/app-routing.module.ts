import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { ApidocComponent } from './apidoc/apidoc.component';
import { HomeComponent } from './home/home.component';

const routes: Routes = [
  { path: '',     component: HomeComponent},
  { path: 'api', component: ApidocComponent },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
