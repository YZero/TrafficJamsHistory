const nom = new autoComplete({
    data: {                              // Data src [Array, Function, Async] | (REQUIRED)
        src: async () => {
            const query = document.querySelector("#autoComplete").value;
            // Fetch External Data Source
            const source = await fetch(`/nomenclature/?q=${query}`);
            // Format data into JSON
            const data = await source.json();
            // Return Fetched data
            return data.nomenclature;
        },
        key: ["name"],
        cache: false
    },
    placeHolder: "Наименование вещи",     // Place Holder text                 | (Optional)
    resultsList: {                       // Rendered results list object      | (Optional)
        render: true,
        container: source => {
            source.setAttribute("id", "nomenclature_list");
        },
        destination: document.querySelector(".results"),
        position: "afterbegin",
        element: "ul"
    },
    resultItem: {                          // Rendered result item            | (Optional)
        content: (data, source) => {
            source.innerHTML = data.match;
        },
        element: "li"
    },
    noResults: () => {                     // Action script on noResults      | (Optional)
        document.querySelector(".selection_nomenclature").innerHTML = 'Новая запись: ' + document.querySelector("#autoComplete").value;
        document.querySelector("#id_nomenclature").value = '';
    },
    onSelection: feedback => {
        document.querySelector(".selection_nomenclature").innerHTML = feedback.selection.value.name;
        document.querySelector("#id_nomenclature").value = feedback.selection.value.id;
        document.querySelector("#autoComplete").value = "";
    }
});

const unit = new autoComplete({
    data: {                              // Data src [Array, Function, Async] | (REQUIRED)
        src: async () => {

            const query = document.querySelector("#unitAutoComplete").value;
            // Fetch External Data Source
            const source = await fetch(`/units/?q=${query}`);
            // Format data into JSON
            const data = await source.json();
            // Return Fetched data
            return data.units;
        },
        key: ["name"],
        cache: false
    },
    selector: "#unitAutoComplete",
    placeHolder: "Наименование ед. изм.",     // Place Holder text                 | (Optional)
    resultsList: {                       // Rendered results list object      | (Optional)
        render: true,
        container: source => {
            source.setAttribute("id", "unit_list");
        },
        destination: document.querySelector(".results"),
        position: "afterbegin",
        element: "ul"
    },
    resultItem: {                          // Rendered result item            | (Optional)
        content: (data, source) => {
            source.innerHTML = data.match;
        },
        element: "li"
    },
    noResults: () => {                     // Action script on noResults      | (Optional)
        document.querySelector(".selection_unit").innerHTML = 'Новая запись: ' + document.querySelector("#unitAutoComplete").value;
        document.querySelector("#id_unit").value = '';
    },
    onSelection: feedback => {
        document.querySelector(".selection_unit").innerHTML = feedback.selection.value.name;
        document.querySelector("#id_unit").value = feedback.selection.value.id;
        // Clear Input
        document.querySelector("#unitAutoComplete").value = "";
    }
});
