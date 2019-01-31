<template>
  <div>
    <b-form inline>
      <label class="sr-only" for="inlineFormInputName2">from</label>
      <b-input class="mb-2 mr-sm-2 mb-sm-0" id="inlineFormInputName2" placeholder="from"/>
      <label class="sr-only" for="inlineFormInputGroupUsername2">to</label>
      <b-input-group left="@" class="mb-2 mr-sm-2 mb-sm-0">
        <b-input id="inlineFormInputGroupUsername2" placeholder="to"/>
      </b-input-group>
      <b-form-checkbox class="mb-2 mr-sm-2 mb-sm-0">Remember me</b-form-checkbox>
      <b-button variant="primary">Search</b-button>
    </b-form>
  </div>
</template>
