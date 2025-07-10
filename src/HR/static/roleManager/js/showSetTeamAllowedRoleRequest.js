if (permisionDataJson.status == "READONLY") {
  $(".editIcon").attr("isDisabled", "true").css("cursor", "not-allowed");
  $(".icon").attr("isDisabled", "true").css("cursor", "not-allowed");
}

// تو اینجا به اینپوت "ظرفیت باقی مانده" مقدار میدیم
$(document).ready(function () {
  const allowedParents = $("#tbody").find("td[teamCode]");
  allowedParents.each(function () {
    inputes = $("input", $(this));
    calculateLowerInputValue($(inputes[0]), $(inputes[2]), $(inputes[3]));
  });
});

// برای قسمتی که اطلاعات ظرفیت کل و نفرات فعلی را نشان میدهد
// در این قسمت رنگ پس زمینه و اتربیوت نفرات فعلی تغییر میکند
$(document).ready(function () {
  $(document).on("mouseenter", "#allowedParent", function () {
    var currentBg = $(this).css("background-color");
    if (!$(this).data("bgColor")) {
      $(this).data("bgColor", currentBg);
    }
    var darkerBg = darkenColor(currentBg, 50);
    $(this).css("background-color", darkerBg);
  });

  $(document).on("mouseleave", "#allowedParent", function () {
    $(this).css("background-color", $(this).data("bgColor"));
  });

  $(document).on("input", ".allowedParentChangeInput", function () {
    if ($(this).val() != $(this).attr("prevValue")) {
      $(this).attr("modified", true);
      const parent = $(this).closest("#allowedParent");
      $(parent)
        .css("background-color", "rgb(0, 150, 0)")
        .data("bgColor", "rgb(0, 150, 0)");
      $(parent)
        .children("p")
        .each(function () {
          $(this).css("color", "white");
        });
      if (isLightColor($(this).css("background-color"))) {
        $(this).css("color", "black");
      } else {
        $(this).css("color", "white");
      }
    } else {
      $(this).attr("modified", false);
      const parent = $(this).closest("#allowedParent");
      if ($(this).attr("prevValue") == 0) {
        $(this).val($(this).attr("prevValue"));
        $(parent).css("background-color", "#c3cbd9").data("bgColor", "#c3cbd9");
      } else {
        $(this).val($(this).attr("prevValue"));
        $(parent)
          .css("background-color", "#6b92e7cc")
          .data("bgColor", "#6b92e7cc");
      }
    }
    if ($(this).val() < 0) {
      $(this).val(0);
    } else if ($(this).val() > 100) {
      $(this).val(100);
    }
  });
});

// برای دکمه های حذف سمت و تیم
$(document).ready(function () {
  // حذف تیم
  $(document).on("click", "#deleteTeam", function () {
    if ($(this).attr("isDisabled") == "false") {
      const teamCode = $(this).attr("teamCode");
      const teamName = $(`th[teamCode=${teamCode}] p#teamName`).text();
      const teamItem = $("<div>")
        .attr({
          teamCode: teamCode,
          class: "team-item",
        })
        .text(teamName);

      $(`th[teamCode=${teamCode}]`).fadeOut(500, function () {
        $(this).remove();
      });
      $(`td[teamCode=${teamCode}]`).fadeOut(500, function () {
        $(this).remove();
      });
    }
  });
  // حذف سمت
  $(document).on("click", "#deleteRole", function () {
    if ($(this).attr("isDisabled") == "false") {
      const roleID = $(this).attr("roleID");
      const roleName = $(`tr[roleID=${roleID}] p#roleID`).text();
      const roleItem = $("<div>")
        .attr({
          roleID: roleID,
          class: "role-item",
        })
        .text(roleName);

      $(`tr[roleID = ${roleID}]`).fadeOut(500, function () {
        $(this).remove();
      });
    }
  });
});

// برای آیکون مداد، که وقتی روی اون کلیک میشه اینپوت تغییر نماییان میشه
$(document).ready(function () {
  $(document).on("click", ".editIcon", function () {
    if ($(this).attr("isDisabled") == "false") {
      const selectedRow = $("#tbody").find(
        `tr[roleId='${$(this).attr("roleID")}']`
      );
      const selectedContainer = selectedRow.find(
        `td[teamCode='${$(this).attr("teamCode")}']`
      );
      selectedContainer.find("#lowerContainer").slideUp("slow", function () {
        selectedContainer
          .find("#hiddenContainer")
          .slideDown("slow", function () {
            $(this).css("display", "flex");
          });
      });
    }
  });
});

// دکمه تایید یا رد درخواست
$(document).ready(function () {
  let DATA = {
    status: "REJECT",
    teamAllowedRoles: [],
  };
  $("#acceptRequest").click(function () {
    $.alert({
      title: "آیا از تایید این درخواست مطمئن هستید؟ ❗",
      content: "این عملیات غیر قابل بازگشت است.",
      type: "orange",
      theme: "modern",
      boxWidth: "400px",
      useBootstrap: false,
      buttons: {
        confirm: {
          text: "بله، مطمئنم",
          btnClass: "btn-green",
          action: function () {
            $(".allowedParentChangeInput[modified='true']").each(function () {
              DATA.status = "ACCEPT";
              const teamCode = $(this).attr("teamCode");
              const roleId = $(this).attr("roleID");
              const value = $(this).val();
              const prevValue = $(this).attr("prevValue");

              let team = DATA.teamAllowedRoles.find(
                (val) => val.TeamCode === teamCode
              );
              if (!team) {
                DATA.teamAllowedRoles.push({
                  TeamCode: teamCode,
                  Roles: [
                    {
                      RoleId: roleId,
                      RoleCount: value,
                      PrevRoleCount: prevValue,
                    },
                  ],
                });
              } else {
                team.Roles.push({
                  RoleId: roleId,
                  RoleCount: value,
                  PrevRoleCount: prevValue,
                });
              }
            });
            $.ajax({
              url: window.location.href,
              type: "POST",
              data: JSON.stringify(DATA),
              contentType: "application/json",
              headers: {
                "X-CSRFToken": $("meta[name='csrf_holder']").attr("content"),
                "Content-Type": "application/json",
              },
              beforeSend: function () {
                $.LoadingOverlay("show");
              },
              complete: function () {
                $.LoadingOverlay("hide");
              },
              success: function (response) {
                let error = response.error;
                $.confirm({
                  title: error ? "❌ خطا" : "✅ موفقیت",
                  content: response.message,
                  type: error ? "red" : "green",
                  theme: "modern",
                  columnClass: "medium",
                  boxWidth: "400px",
                  useBootstrap: false,
                  buttons: {
                    ok: {
                      text: "باشه",
                      btnClass: error ? "btn-red" : "btn-green",
                      action: function () {
                        $.LoadingOverlay("show");
                        window.location.reload();
                      },
                    },
                  },
                });
              },
              error: function (error) {
                $.confirm({
                  title: "❌ خطا در ارتباط",
                  content: "خطایی در ارتباط با سرور رخ داده است.",
                  type: "red",
                  theme: "modern",
                  columnClass: "medium",
                  boxWidth: "400px",
                  useBootstrap: false,
                  buttons: {
                    ok: {
                      text: "باشه",
                      btnClass: "btn-red",
                    },
                  },
                });
              },
            });
          },
        },
        cancel: {
          text: "لغو",
          btnClass: "btn-default",
        },
      },
    });
  });
  $("#rejectRequest").click(function () {
    $.alert({
      title: "آیا از رد این درخواست مطمئن هستید؟ ❗",
      content: "این عملیات غیر قابل بازگشت است.",
      type: "orange",
      theme: "modern",
      boxWidth: "400px",
      useBootstrap: false,
      buttons: {
        confirm: {
          text: "بله، مطمئنم",
          btnClass: "btn-red",
          action: function () {
            $.ajax({
              url: window.location.href,
              type: "POST",
              data: JSON.stringify(DATA),
              contentType: "application/json",
              headers: {
                "X-CSRFToken": $("meta[name='csrf_holder']").attr("content"),
                "Content-Type": "application/json",
              },
              beforeSend: function () {
                $.LoadingOverlay("show");
              },
              complete: function () {
                $.LoadingOverlay("hide");
              },
              success: function (response) {
                let error = response.error;
                $.confirm({
                  title: error ? "❌ خطا" : "✅ موفقیت",
                  content: response.message,
                  type: error ? "red" : "green",
                  theme: "modern",
                  columnClass: "medium",
                  boxWidth: "400px",
                  useBootstrap: false,
                  buttons: {
                    ok: {
                      text: "باشه",
                      btnClass: error ? "btn-red" : "btn-green",
                      action: function () {
                        $.LoadingOverlay("show");
                        window.location.reload();
                      },
                    },
                  },
                });
              },
              error: function (error) {
                $.confirm({
                  title: "❌ خطا در ارتباط",
                  content: "خطایی در ارتباط با سرور رخ داده است.",
                  type: "red",
                  theme: "modern",
                  columnClass: "medium",
                  boxWidth: "400px",
                  useBootstrap: false,
                  buttons: {
                    ok: {
                      text: "باشه",
                      btnClass: "btn-red",
                    },
                  },
                });
              },
            });
          },
        },
        cancel: {
          text: "لغو",
          btnClass: "btn-default",
        },
      },
    });
  });
});

// --------------------------------------------- FUNCTIONS ---------------------------------------------
//  تغییر رنک سلول وقتی که هاور میشه روش
function darkenColor(color, amount) {
  var col = color.match(/\d+/g);
  var r = Math.min(255, parseInt(col[0]) - amount);
  var g = Math.min(255, parseInt(col[1]) - amount);
  var b = Math.min(255, parseInt(col[2]) - amount);
  return "rgb(" + r + "," + g + "," + b + ")";
}
function isLightColor(color) {
  var rgb = color.match(/^rgba?\((\d+), (\d+), (\d+)/);

  if (rgb) {
    var r = parseInt(rgb[1]);
    var g = parseInt(rgb[2]);
    var b = parseInt(rgb[3]);
    var brightness = 0.2126 * r + 0.7152 * g + 0.0722 * b;

    return brightness > 128;
  }
  return false;
}
// محاسبه ظرفیت کل و نفرات فعلی
function calculateLowerInputValue(upperInput, middleInput, lowerInput) {
  const up = parseFloat(upperInput.val()) || 0;
  const mid = parseFloat(middleInput.val()) || 0;
  let result = up - mid;
  if (result < 0) {
    lowerInput.val(0);
  } else {
    lowerInput.val(result);
  }
}
