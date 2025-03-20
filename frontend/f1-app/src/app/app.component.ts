import { Component, AfterViewInit } from '@angular/core';
import axios from 'axios';
import Chart from 'chart.js/auto';

@Component({
  selector: 'app-root',
  template: `
    <div class="container">
      <h1>F1 Race Predictions</h1>

      <!-- Table for Race Winners -->
      <table *ngIf="raceData.length">
        <tr>
          <th>Race</th>
          <th>Winner</th>
          <th>Constructor</th>
          <th>Grid Position</th>
        </tr>
        <tr *ngFor="let race of raceData">
          <td>{{ race.Race }}</td>
          <td>{{ race.Driver }}</td>
          <td>{{ race.Constructor }}</td>
          <td>{{ race['Grid Position'] }}</td>
        </tr>
      </table>

      <!-- Form to Predict Winner -->
      <div>
        <label>Constructor:</label>
        <input [(ngModel)]="constructorInput" placeholder="Red Bull" />
        <label>Grid Position:</label>
        <input type="number" [(ngModel)]="gridPositionInput" placeholder="1" />
        <button (click)="predictWinner()">Predict Winner</button>
      </div>

      <h2 *ngIf="predictedWinner">Predicted Winner: {{ predictedWinner }}</h2>

      <!-- Chart for Predicted Winners -->
      <canvas id="f1Chart"></canvas>
    </div>
  `,
  styles: [`
    .container { text-align: center; margin: 20px; }
    table { width: 100%; border-collapse: collapse; margin-top: 20px; }
    th, td { border: 1px solid #ddd; padding: 10px; text-align: left; }
    th { background-color: #f4f4f4; }
  `]
})
export class AppComponent implements AfterViewInit {
  raceData: any[] = [];
  predictedWinner: string = '';
  constructorInput: string = '';
  gridPositionInput: number = 1;
  chart: any;

  async ngAfterViewInit() {
    try {
      const response = await axios.get('http://127.0.0.1:8000/f1-data');
      this.raceData = response.data;
      this.createChart();
    } catch (error) {
      console.error("Error fetching race data:", error);
    }
  }

  async predictWinner() {
    try {
      const response = await axios.get(`http://127.0.0.1:8000/predict?constructor=${this.constructorInput}&grid_position=${this.gridPositionInput}`);
      this.predictedWinner = response.data['Predicted Winner'];

      // Update chart with the predicted winner
      this.updateChart(this.predictedWinner);
    } catch (error) {
      console.error("Prediction error:", error);
    }
  }

  createChart() {
    const driverWins: { [key: string]: number } = {};

    this.raceData.forEach(race => {
      driverWins[race.Driver] = (driverWins[race.Driver] || 0) + 1;
    });

    const drivers = Object.keys(driverWins);
    const wins = Object.values(driverWins);

    this.chart = new Chart("f1Chart", {
      type: 'bar',
      data: {
        labels: drivers,
        datasets: [{
          label: 'Race Wins',
          data: wins,
          backgroundColor: 'rgba(75, 192, 192, 0.6)',
          borderColor: 'rgba(75, 192, 192, 1)',
          borderWidth: 1
        }]
      }
    });
  }

  updateChart(predictedWinner: string) {
    if (this.chart) {
      const index = this.chart.data.labels.indexOf(predictedWinner);
      if (index !== -1) {
        this.chart.data.datasets[0].data[index] += 1; // Increment win count if driver exists
      } else {
        this.chart.data.labels.push(predictedWinner);
        this.chart.data.datasets[0].data.push(1); // Add a new driver with 1 win
      }
      this.chart.update(); // Refresh chart
    }
  }
}
