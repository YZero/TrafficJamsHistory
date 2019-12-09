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
        const result = document.createElement("li");
        result.setAttribute("class", "no_result");
        result.setAttribute("tabindex", "1");
        result.innerHTML = "No Results";
        document.querySelector("#nomenclature_list").appendChild(result);
    },
    onSelection: feedback => {
        const selection = feedback.selection.value.name;
        // Render selected choice to selection div
        document.querySelector(".selection_nomenclature").innerHTML = selection;
        document.querySelector(".input_nomenclature_id").value = feedback.selection.value.id;
        // Clear Input
        document.querySelector("#autoComplete").value = "";
        // Change placeholder with the selected value
        document
            .querySelector("#autoComplete")
            .setAttribute("placeholder", selection);
        // Action script onSelection event | (Optional)
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
        const result = document.createElement("li");
        result.setAttribute("class", "no_result");
        result.setAttribute("tabindex", "1");
        result.innerHTML = "No Results2";
        document.querySelector("#unit_list").appendChild(result);
    },
    onSelection: feedback => {
        const selection = feedback.selection.value.name;
        // Render selected choice to selection div
        document.querySelector(".selection_unit").innerHTML = selection;
        document.querySelector(".input_unit_id").value = feedback.selection.value.id;
        // Clear Input
        document.querySelector("#unitAutoComplete").value = "";
        // Change placeholder with the selected value
        document
            .querySelector("#unitAutoComplete")
            .setAttribute("placeholder", selection);
        // Action script onSelection event | (Optional)
    }
});
