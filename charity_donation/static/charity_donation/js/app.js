document.addEventListener("DOMContentLoaded", function() {
  /**
   * HomePage - Help section
   */

  function show_organization(ids) {
        var address = '/get_institution_by_category/';
        var data2 = {'cat_id':ids};
        $.ajax(address, {data: data2, traditional:true}).success( function (data, status) {
        $('#institution').html(data);
        });

}

  function form_validation() {

      if(($('input[name="categories"]:checked').length) == 0){
      alert("Wybierz co najmniej jedną kategorię");
      return false;
      };

      if(document.form.bags.value == "") {
      alert("Uzupełnij liczbę worków");
      return false;
      };

      if($('input[name="organization"]:checked').val() == undefined){
        alert("Wybierz organizację, której chcesz przekazać dary");
        return false;
      };

      if(document.form.address.value == "") {
      alert("Uzupełnij adres");
      return false;
      };

      if(document.form.city.value == "") {
      alert("Uzupełnij miasto");
      return false;
      };

      var postcode_format = /^\d{2}-\d{3}$/;
      if(document.form.postcode.value == "" || !document.form.postcode.value.match(postcode_format)) {
      alert("Uzupełnij kod pocztowy w formacie xx-xxx");
      return false;
      };

      var phone_format = /^\d{9}$/;
      if(!document.form.phone.value.match(phone_format)) {
      alert("Wprowadź 9 cyfrowy numer telefonu");
      return false;
      };

      if(document.form.date.value == "") {
        alert("Wybierz datę odbioru");
        return false;
      };

      var date = document.form.date.value;
      var varDate = new Date(date);
      var today = new Date();
      if(varDate <= today) {
        alert("Data nie może być wcześniejsza od dzisiejszej");
        return false;
      };

      if(document.form.time.value == "") {
      alert("Wybierz godzinę odbioru");
      return false;
      };

      return(true);
}

  class Help {
    constructor($el) {
      this.$el = $el;
      this.$buttonsContainer = $el.querySelector(".help--buttons");
      this.$slidesContainers = $el.querySelectorAll(".help--slides");
      this.currentSlide = this.$buttonsContainer.querySelector(".active").parentElement.dataset.id;
      this.init();
    }

    init() {
      this.events();
    }

    events() {
      /**
       * Slide buttons
       */
      this.$buttonsContainer.addEventListener("click", e => {
        if (e.target.classList.contains("btn")) {
          this.changeSlide(e);
        }
      });

      /**
       * Pagination buttons
       */
      this.$el.addEventListener("click", e => {
        if (e.target.classList.contains("btn") && e.target.parentElement.parentElement.classList.contains("help--slides-pagination")) {
          this.changePage(e);
        }
      });
    }

    changeSlide(e) {
      e.preventDefault();
      const $btn = e.target;

      // Buttons Active class change
      [...this.$buttonsContainer.children].forEach(btn => btn.firstElementChild.classList.remove("active"));
      $btn.classList.add("active");

      // Current slide
      this.currentSlide = $btn.parentElement.dataset.id;

      // Slides active class change
      this.$slidesContainers.forEach(el => {
        el.classList.remove("active");

        if (el.dataset.id === this.currentSlide) {
          el.classList.add("active");
        }
      });
    }

    /**
     * TODO: callback to page change event
     */
    changePage(e) {
      e.preventDefault();
      const page = e.target.dataset.page;

      console.log(page);
    }
  }
  const helpSection = document.querySelector(".help");
  if (helpSection !== null) {
    new Help(helpSection);
  }

  /**
   * Form Select
   */
  class FormSelect {
    constructor($el) {
      this.$el = $el;
      this.options = [...$el.children];
      this.init();
    }

    init() {
      this.createElements();
      this.addEvents();
      this.$el.parentElement.removeChild(this.$el);
    }

    createElements() {
      // Input for value
      this.valueInput = document.createElement("input");
      this.valueInput.type = "text";
      this.valueInput.name = this.$el.name;

      // Dropdown container
      this.dropdown = document.createElement("div");
      this.dropdown.classList.add("dropdown");

      // List container
      this.ul = document.createElement("ul");

      // All list options
      this.options.forEach((el, i) => {
        const li = document.createElement("li");
        li.dataset.value = el.value;
        li.innerText = el.innerText;

        if (i === 0) {
          // First clickable option
          this.current = document.createElement("div");
          this.current.innerText = el.innerText;
          this.dropdown.appendChild(this.current);
          this.valueInput.value = el.value;
          li.classList.add("selected");
        }

        this.ul.appendChild(li);
      });

      this.dropdown.appendChild(this.ul);
      this.dropdown.appendChild(this.valueInput);
      this.$el.parentElement.appendChild(this.dropdown);
    }

    addEvents() {
      this.dropdown.addEventListener("click", e => {
        const target = e.target;
        this.dropdown.classList.toggle("selecting");

        // Save new value only when clicked on li
        if (target.tagName === "LI") {
          this.valueInput.value = target.dataset.value;
          this.current.innerText = target.innerText;
        }
      });
    }
  }
  document.querySelectorAll(".form-group--dropdown select").forEach(el => {
    new FormSelect(el);
  });

  /**
   * Hide elements when clicked on document
   */
  document.addEventListener("click", function(e) {
    const target = e.target;
    const tagName = target.tagName;

    if (target.classList.contains("dropdown")) return false;

    if (tagName === "LI" && target.parentElement.parentElement.classList.contains("dropdown")) {
      return false;
    }

    if (tagName === "DIV" && target.parentElement.classList.contains("dropdown")) {
      return false;
    }

    document.querySelectorAll(".form-group--dropdown .dropdown").forEach(el => {
      el.classList.remove("selecting");
    });
  });

  /**
   * Switching between form steps
   */
  class FormSteps {
    constructor(form) {
      this.$form = form;
      this.$next = form.querySelectorAll(".next-step");
      this.$prev = form.querySelectorAll(".prev-step");
      this.$step = form.querySelector(".form--steps-counter span");
      this.currentStep = 1;

      this.$stepInstructions = form.querySelectorAll(".form--steps-instructions p");
      const $stepForms = form.querySelectorAll("form > div");
      this.slides = [...this.$stepInstructions, ...$stepForms];

      this.init();
    }

    /**
     * Init all methods
     */
    init() {
      this.events();
      this.updateForm();
    }

    /**
     * All events that are happening in form
     */
    events() {
      // Next step
      this.$next.forEach(btn => {
        btn.addEventListener("click", e => {
          e.preventDefault();
          this.currentStep++;
          this.updateForm();
        });
      });

      // Previous step
      this.$prev.forEach(btn => {
        btn.addEventListener("click", e => {
          e.preventDefault();
          this.currentStep--;
          this.updateForm();
        });
      });

      // Form submit
      this.$form.querySelector("form").addEventListener("submit", e => this.submit(e));
    }

    /**
     * Update form front-end
     * Show next or previous section etc.
     */
    updateForm() {
      this.$step.innerText = this.currentStep;

      // TODO: Validation

      if (this.currentStep == 3){
        var ids = [];
        $('input[name="categories"]:checked').each(function() {
            ids.push(this.value);
      })
        // console.log(ids)
        show_organization(ids)
      }

      this.slides.forEach(slide => {
        slide.classList.remove("active");

        if (slide.dataset.step == this.currentStep) {
          slide.classList.add("active");
        }
      });

      this.$stepInstructions[0].parentElement.parentElement.hidden = this.currentStep >= 6;
      this.$step.parentElement.hidden = this.currentStep >= 6;


      // TODO: get data from inputs and show them in summary


      if (this.currentStep == 5){
        var bags = $('input[name="bags"]').val();
        var bags_span = $("#bags")[0];
        bags_span.innerText = bags_span.textContent = 'Liczba worków: ' + bags;


        var organization = $('input[name="organization"]:checked').attr('my-attr');
        var org_span = $("#organization")[0];
        org_span.innerText = "Dla: " + organization;

        var address = $('input[name="address"]').val();
        var address_li = $("#address")[0];
        address_li.innerText = address;

        var city = $('input[name="city"]').val();
        var city_li = $("#city")[0];
        city_li.innerText = city;

        var postcode = $('input[name="postcode"]').val();
        var postcode_li = $("#postcode")[0];
        postcode_li.innerText = postcode;

        var phone = $('input[name="phone"]').val();
        var phone_li = $("#phone")[0];
        phone_li.innerText = phone;

        var date = $('input[name="date"]').val();
        var date_li = $("#date")[0];
        date_li.innerText = date;

        var time = $('input[name="time"]').val();
        var time_li = $("#time")[0];
        time_li.innerText = time;

        var more_info = $('textarea[name="more_info"]').val();
        var more_info_li = $("#more-info")[0];
        more_info_li.innerText = more_info;
      }

    }

    /**
     * Submit form
     *
     * TODO: validation, send data to server
     */

    submit(e) {
      // e.preventDefault();
      if (form_validation() == false) {
        e.preventDefault();
      } else {
        this.currentStep++;
        this.updateForm();
      }
    }

  }
  const form = document.querySelector(".form--steps");
  if (form !== null) {
    new FormSteps(form);
  }
});
