<template>
  <div>
    <b-form inline class="onTopOf" @submit="onSubmit" @reset="onReset" v-if="showForm">
      <b-container class="bv-example-row">
        <b-row>
          <b-col>
            <b-form-group id="exampleInputGroup1"
                          label="fromCity"
                          class="label-text-align"
                          label-for="exampleInput1">
              <b-form-input id="exampleInput1"
                            type="text"
                            v-model="form.fromCity"
                            required
                            placeholder="from">
              </b-form-input>
            </b-form-group>
          </b-col>
          <b-col>
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
          </b-col>
          <b-col>
            <h6>Select a date</h6>
            <datetime type="datetime"
                      v-model="form.datetime"
                      title="Select the date"></datetime>
            </b-col>
          <b-col>

            <b-button type="submit" variant="primary">Submit</b-button>
          <br/>
            <b-button type="reset" variant="danger">Reset</b-button>

          </b-col>
        </b-row>
      </b-container>
    </b-form>
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
            <button type="button" class="btn btn-warning btn-sm">Buy tickets {{ price | formatPrice}} €</button>
          </td>
        </tr>
        </tbody>
      </table>
  </div>
</template>

<script>
  import axios from 'axios';

  export default {
    data() {
      return {
        form: {
          fromCity: '',
          toCity: '',
          datetime: new Date().toISOString().slice(0, 10),
        },
        journeys: {},
        showForm: true,
        showJourneys: false,
      }
    },
    methods: {
      lookUpTrains(payload) {
        const path = 'https://trouvetrain.azurewebsites.net/Trains';
        axios.get(path, payload)
          .then((res) => {
            this.journeys = res.data.journeys;
            this.price = res.data.price;
            this.showJourneys = true;
          })
          .catch((error) => {
            // eslint-disable-next-line
            console.error(error);
          });
      },
      onSubmit(evt) {
        console.log(this.form.datetime);
        evt.preventDefault();
        //alert(JSON.stringify(this.form));
        const payload = {
          params: {
            fromCity: this.form.fromCity,
            toCity: this.form.toCity,
            datetime: this.form.datetime,
          }
        };
        this.lookUpTrains(payload);
      },
      onReset(evt) {
        evt.preventDefault();
        /* Reset our form values */
        this.form.fromCity = '';
        this.form.toCity = '';
        this.form.date = new Date().toISOString().slice(0, 10);
        /* Trick to reset/clear native browser form validation state */
        this.showForm = false;
        this.$nextTick(() => {
          this.showForm = true
        });
        this.showJourneys = false;
      }
    }
  }

</script>

<style>
  .onTopOf{
    box-shadow: 0 4px 2px -2px gray;
     padding-bottom: 45px;
  }
</style>
