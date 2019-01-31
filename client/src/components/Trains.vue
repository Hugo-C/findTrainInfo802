<template>
  <div>
    <b-form @submit="onSubmit" @reset="onReset" v-if="showForm">
      <b-form-group id="exampleInputGroup1"
                    label="fromCity"
                    label-for="exampleInput1"
                    description="Enter the first letters of the city from where you want to start your journey.">
        <b-form-input id="exampleInput1"
                      type="text"
                      v-model="form.fromCity"
                      required
                      placeholder="from">
        </b-form-input>
      </b-form-group>
      <b-form-group id="exampleInputGroup2"
                    label="toCity"
                    label-for="exampleInput2">
        <b-form-input id="exampleInput2"
                      type="text"
                      v-model="form.toCity"
                      required
                      placeholder="to">
        </b-form-input>
      </b-form-group>
      <b-button type="submit" variant="primary">Submit</b-button>
      <b-button type="reset" variant="danger">Reset</b-button>
    </b-form>
    <br><br>
    <table class="table table-hover" v-if="showJourneys">
          <thead>
          <tr>
            <th scope="col">departure_date</th>
            <th scope="col">arrival_date</th>
            <th scope="col">duration</th>
            <th></th>
          </tr>
          </thead>
          <tbody>
          <tr v-for="(journey, index) in journeys" :key="index">
            <td>{{ journey.departure_date | formatDate}}</td>
            <td>{{ journey.arrival_date | formatDate}}</td>
            <td>{{ journey.duration | formatDuration }}</td>
            <td>
              <button type="button" class="btn btn-warning btn-sm">Buy tickets</button>
            </td>
          </tr>
          </tbody>
        </table>
  </div>
</template>

<script>
  import axios from 'axios';

  export default {
    data () {
      return {
        form: {
          fromCity: '',
          toCity: '',
        },
        journeys:{

        },
        showForm: true,
        showJourneys: false,
      }
    },
    methods: {
      lookUpTrains(payload) {
        const path = 'http://localhost:5000/Trains';
        axios.get(path, payload)
          .then((res) => {
            this.journeys = res.data.journeys;
            this.showJourneys = true;
          })
          .catch((error) => {
            // eslint-disable-next-line
            console.error(error);
          });
      },
      onSubmit (evt) {
        evt.preventDefault();
        //alert(JSON.stringify(this.form));
        const payload = {
          params: {
            fromCity: this.form.fromCity,
            toCity: this.form.toCity,
          }
        };
        this.lookUpTrains(payload);
      },
      onReset (evt) {
        evt.preventDefault();
        /* Reset our form values */
        this.form.fromCity = '';
        this.form.toCity = '';
        /* Trick to reset/clear native browser form validation state */
        this.showForm = false;
        this.$nextTick(() => { this.showForm = true });
        this.showJourneys = false;
      }
    }
  }

</script>

<!-- b-form-1.vue -->
