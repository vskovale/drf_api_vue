<template>
  <div id="app">
    <h1>Изображения на сервере</h1>
    <form @submit.prevent="uploadImage">
      <input type="text" v-model="description" placeholder="Описание">
      <input type="file" @change="onFileChange">
      <button type="submit">Загрузить</button>
    </form>
    <div v-for="image in images" :key="image.id">
      <img :src=image.image_data alt="image">
      <p>{{ image.description }}</p>
      <button @click="deleteImage(image.id)">Удалить</button>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      description: '',
      image: null,
      images: []
    };
  },
  mounted() {
    this.fetchImages();
  },
  methods: {
    onFileChange(event) {
      this.image = event.target.files[0];
    },
 uploadImage() {
      let formData = new FormData();
      formData.append('description', this.description);
      let reader = new FileReader();
      reader.readAsDataURL(this.image);
      reader.onload = () => {
        formData.append('image_data', reader.result);
        axios.post('http://localhost:8000/api/', formData)
          .then(response => {
            console.log(response.data);
            this.fetchImages();
          })
          .catch(error => {
            console.error('Error:', error, formData);
          });
      };
    },
    fetchImages() {
      axios.get('http://localhost:8000/api/')
        .then(response => {
          this.images = response.data;
        })
        .catch(error => {
          console.error('Error:', error, this.images);
        });
    },
    deleteImage(id) {
      axios.delete(`http://localhost:8000/api/${id}/`)
        .then(response => {
          console.log(response.data);
          this.fetchImages();
        })
        .catch(error => {
          console.error('Error:', error);
        });
    }
  }
};
</script>

<style>
#app {
  text-align: center;
}
</style>
