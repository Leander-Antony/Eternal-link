$(document).ready(function() {
    $("#flamesForm").submit(function(event) {
        event.preventDefault(); 
        const formData = $(this).serialize(); 
        $.post("/submit", formData, function(data) {
            $("#resultText").text("Your relationship status is: " + data.result);

            let imageUrl = "";
            switch (data.result) {
                case "Friends":
                    imageUrl = "./static/images/friends.jpg"; 
                    break;
                case "Love":
                    imageUrl = "./static/images/love.jpg";
                    break;
                case "Affection":
                    imageUrl = "./static/images/affection.jpg"; 
                    break;
                case "Marriage":
                    imageUrl = "./static/images/marriage.jpg"; 
                    break;
                case "Enemy":
                    imageUrl = "./static/images/enemy.jpg"; 
                    break;
                case "Siblings":
                    imageUrl = "./static/images/sibling.jpg"; 
                    break;
            }

            $("#resultImage").attr("src", imageUrl);
            $("#resultModal").modal('show');
            $("#questionModal").modal('hide');
        });
    });
});