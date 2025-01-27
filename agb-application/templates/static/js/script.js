function getDefaultValue() {
         const now = new Date();
         let year = now.getFullYear();
         let month = (now.getMonth() + 1).toString().padStart(2, '0');
         let day = now.getDate().toString().padStart(2, '0');
         let hour = now.getHours().toString().padStart(2, '0');
         let minute = now.getMinutes().toString().padStart(2, '0');

         return `${year}-${month}-${day}T${hour}:${minute}`;
       }