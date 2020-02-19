$(document).ready(function() {
    /* activeer de checkboxes, klikken is kiezen. */
    $('.skill').click(function() {
        that = this;
        urlParams = new URLSearchParams(window.location.search);
        q = urlParams.get('q');
        if (that.checked) {
            if (q) { q = q + ' ' + that.value.toLowerCase(); }
            else   { q = that.value.toLowerCase(); }
        }
        else {
            ar.forEach(function(item, index, object) {
                if (item.toLowerCase() == that.value.toLowerCase()) {
                    object.splice(index,1)}
            });
            q = ar.join(' ');
        }
        urlParams.set('q', q);
        window.location.search = urlParams;
    });

    /* Suggesties activeren voor typen in de zoekbox*/
    $('#q').keyup(function () {
        if (this.value) {
            jQuery.ajax({
                url: '/suggest/' + this.value,
                success: showSuggestions
            });
        }
    });

    $('.row .buckets').click(function() {
        removeSuggestions();
        console.log('clickerdieclick')
    });

    function showSuggestions(data){
        if (!data) {return false;}
        removeSuggestions()
        a = document.createElement("div");
        a.setAttribute('id', 'q-autocomplete');
        document.getElementById('suggestions').appendChild(a);
        data.forEach(function(item, index) {
            i = document.createElement('div');
            i.innerHTML = item;
            i.addEventListener('click',function(){
                $('#q').val(this.innerText);
                removeSuggestions()
            });
            a.appendChild(i);
        });
    }

    function removeSuggestions() {
        old = document.getElementById('q-autocomplete');
        if (old) {old.remove();}
    }
});
