import { Component, OnInit } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import Chart from 'chart.js/auto';
import axios from 'axios';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css',
  template: `<canvas id="f1Chart"></canvas>`
})
export class AppComponent {
  title = 'f1-app';

  data: any;

  async ngOnInit() {
    try {
      const response = await axios.get('http://ergast.com/api/f1/2023/results.json');
      this.data = response.data;
    } catch (error) {
      console.error(error);
    }
  }

  async ngAfterViewInit() {
    const response = await axios.get('http://ergast.com/api/f1/2023/results.json');
    const raceNames = response.data.MRData.RaceTable.Races.map((race: any) => race.raceName);
    const rounds = response.data.MRData.RaceTable.Races.map((race: any) => race.round);

    new Chart("f1Chart", {
      type: 'bar',
      data: {
        labels: raceNames,
        datasets: [{
          label: 'Race Rounds',
          data: rounds,
          backgroundColor: 'rgba(75, 192, 192, 0.2)',
          borderColor: 'rgba(75, 192, 192, 1)',
          borderWidth: 1
        }]
      },
      options: {
        responsive: true,
        scales: { y: { beginAtZero: true } }
      }
    });
  }
}
