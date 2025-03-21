//common function
function showToast(msg) {
  const toastHtml = `<div class="toast" role="alert">
    <div class="toast-header">
      <img src="${V2_STATIC_PATH}/img/logo.jpg" class="rounded me-2" style="height: 1.5rem;">
      <strong class="me-auto">万有真原</strong>
      <button type="button" class="btn-close" data-bs-dismiss="toast" aria-label="Close"></button>
    </div>
    <div class="toast-body">
      ${msg}
    </div>
  </div>`;

  const toast = $(toastHtml);
  $(".toast-container").append(toast);
  toast.toast('show');
};

// pop up bible annotation
function jumpTo(id) {
  const [_, num] = id.split("-");
  const aNum = num || "1";

  var modal = $("#modal-annotation");
  modal.find('.modal-annotation-sup').html($(`#text-ann-${aNum} sup`).text().trim());
  modal.find('.modal-body').html($(id)[0].innerHTML);
  modal.modal('show');
}

(() => {
  'use strict'

  window.util = {
    getLogo: function() {
      return V2_STATIC_PATH + '/img/logo.jpg';
    },
    getUrlParam: function(key) {
      return new URLSearchParams(window.location.search).get(key);
    },
    parseTime: function(time) {
      if(time instanceof Date) {
        return time;
      } else if(typeof time === 'string') {
        //use regex to match yyyy-MM-dd format, and replace '-' with '/'
        const regex = /(\d{4})-(\d{2})-(\d{2})/;
        time = time.replace(regex, '$1/$2/$3');
        return new Date(time);
      } else {
        return new Date(time);
      }
    },
    friendlyNumber: function(num) {
      if (num > 10000) {
        return (num / 10000).toFixed(1) + '万';
      } else if(num > 100000000) {
        return (num / 100000000).toFixed(1) + '亿';
      }
      return num;
    },
    formatDate: function(time, withYear = true) {
      const target = this.parseTime(time);
      const year = target.getFullYear();
      const month = target.getMonth();
      const day = target.getDate();
      return `${withYear ? `${year}年` : ''}${month+1}月${day}日`;
    },
    formatTime: function(time, withSeconds = true) {
      const target = this.parseTime(time);
      const hour = target.getHours();
      const minute = target.getMinutes();
      const second = target.getSeconds();
      return `${hour < 10 ? '0' + hour : hour}:${minute < 10 ? '0' + minute : minute}${withSeconds ? `:${second < 10 ? '0' + second : second}` : ''}`;
    },
    formatDateTime: function(time) {
      const target = this.parseTime(time);
      const year = target.getFullYear();
      const month = target.getMonth();
      const day = target.getDate();
      const hour = target.getHours();
      const minute = target.getMinutes();
      return `${year}-${month+1 < 10 ? '0' + (month+1) : (month+1)}-${day < 10 ? '0' + day : day} ${hour < 10 ? '0' + hour : hour}:${minute < 10 ? '0' + minute : minute}`;
    },
    friendlyDiffDays: function(diffDays) {
      if(diffDays == -2) {
        return '前天';
      } else if(diffDays == -1) {
        return '昨天';
      } else if(diffDays === 0) {
        return '今天';
      } else if(diffDays === 1) {
        return '明天';
      } else if(diffDays === 2) {
        return '后天';
      } else if(diffDays > 2) {
        return `${diffDays}天后`;
      } else {
        return `${diffDays}天前`;
      }
    },
    friendlyTime: function(time) {
      const now = new Date();
      const target = this.parseTime(time);
      
      const nowDays = now.getMonth() * 100 + now.getDate();
      const targetDays = target.getMonth() * 100 + target.getDate();
      const diffDays = targetDays - nowDays;

      if(Math.abs(diffDays) < 3) {
        return `${this.friendlyDiffDays(diffDays)} ${this.formatTime(time, false)}`;
      } else if(Math.abs(diffDays) > 200) {
        return `${this.formatDate(time, true)} ${this.formatTime(time, false)}`;
      } else {
        return `${this.formatDate(time, false)} ${this.formatTime(time, false)}`;
      }
    },
    formatCountDown: function(hours, minutes, seconds) {
      return hours.toString().padStart(2, '0') + ':' + minutes.toString().padStart(2, '0') + ':' + seconds.toString().padStart(2, '0');
    },
    friendlyCountDown: function(time) {
      const now = new Date();
      const diff = this.parseTime(time) - now;
      const diffSeconds = Math.floor((diff / 1000) % 60);
      const diffMinutes = Math.floor((diff / (1000 * 60)) % 60);
      const diffHours = Math.floor((diff / (1000 * 60 * 60)) % 24);
      const diffDays = Math.floor(diff / (1000 * 60 * 60 * 24));
      if(diffDays > 0) {
        return `${diffDays}天 ${this.formatCountDown(diffHours, diffMinutes, diffSeconds)}`;
      } else if(diffDays < 0) {
        return `${Math.abs(diffDays)}天前 ${this.formatCountDown(diffHours, diffMinutes, diffSeconds)}`;
      } else {
        return `${this.formatCountDown(diffHours, diffMinutes, diffSeconds)}`;
      }
    },
    cvtTimeByZone: function(time, zone) {
      const date = this.parseTime(time);
      const utcTime = new Date(Date.UTC(date.getFullYear(), date.getMonth(), date.getDate(), date.getHours()-zone, date.getMinutes(), date.getSeconds()));
      return utcTime;
    },
    cvtChineseTime: function(time) {
      return this.cvtTimeByZone(time, 8);
    },
    cvtLrcToText: function(lrc) {
      if (!lrc) return '';
      const lines = lrc.split('\n').filter(line => line.trim());
      const lyrics = lines.map(line => {
          const timeTagPattern = /\[\d{2}:\d{2}[:.]\d{2,3}\]/g;
          const text = line.replace(timeTagPattern, '').trim();
          if (text.startsWith('[') && text.endsWith(']')) {
              return '';
          }
          return text;
      });
      return lyrics.filter(text => text).join('\n');
    },
    setStorage: function(key, value) {
      localStorage.setItem(key, value);
    },
    getStorage: function(key) {
      return localStorage.getItem(key);
    },
    removeStorage: function(key) {
      localStorage.removeItem(key);
    },
    openApp: function(schema) {
      window.location.href = schema;
    },
    isWxBrowser: function() {
      return /MicroMessenger/i.test(navigator.userAgent);
    },
    updateWxShare: function() {
      if(!this.isWxBrowser()) {
        return;
      }

      const wxData = {
        title: pageMeta.title,
        link: location.href.split('#')[0],
        imgUrl: pageMeta.thumbnail,
        desc: pageMeta.description
      }

      $.ajax({
        url: EASTER_DOMAIN + "api/weixin/jsapi/signature?url=" + encodeURIComponent(wxData.link),
        dataType: "json",
        type: "get",
        success: function(data) {
          wx.config({
            debug: false,
            appId: data.content.appId,
            timestamp: data.content.timestamp,
            nonceStr: data.content.nonceStr,
            signature: data.content.signature,
            jsApiList: [
              'checkJsApi',
              'updateTimelineShareData', 
              'updateAppMessageShareData',
            ],
            openTagList: ["wx-open-launch-app"]
          });
        }
      });

      wx.ready(function() {
        wx.updateTimelineShareData(wxData);
        wx.updateAppMessageShareData(wxData);

        $("wx-open-launch-app").on("error", function (e) {
          window.location.href = APP_DOWNLOAD_URL;
        });
      });
    }
  }
})();

// statistics function
(() => {
  const BusinessType = {
      News: 1,    //article
      Singer: 2,  //singer
      Album: 3,   //album
      Sheet: 4,   //sheet
      Track: 5,   //audio
      ShortUrl: 6,//short url
      Church: 7,  //church
      Saint: 8,   //saint/holiday
      Bible: 9,   //bible
      Person: 10, //personnel
      Custom: 32  //custom
  }
  let statisticDomain = EASTER_DOMAIN;

  function updateRealtimeHits(type, id) {
      $.ajax({
          url: statisticDomain + "api/statistic/realtime",
          type: "post",
          dataType: "json",
          contentType: "application/json; charset=utf-8",
          data: JSON.stringify({
              businessType: type,
              businessId: parseInt(id)
          }),
          success: function (data) {
          }
      });
  }

  window.statistic = {
      updateTrack: function (trackId) {
          return updateRealtimeHits(BusinessType.Track, trackId);
      },
      updateNews: function (newsId) {
          return updateRealtimeHits(BusinessType.News, newsId);
      },
      updateChurch: function (churchId) {
          return updateRealtimeHits(BusinessType.Church, churchId);
      },
      updateSaint: function (saintId) {
          return updateRealtimeHits(BusinessType.Saint, saintId);
      }
  }
})();

// theme switch
(() => {
  'use strict'

  const getStoredTheme = () => util.getStorage('theme')
  const setStoredTheme = theme => util.setStorage('theme', theme)

  const getPreferredTheme = () => {
    const storedTheme = getStoredTheme()
    if (storedTheme) {
      return storedTheme
    }
    return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'
  }

  window.isDark = () => {
    return $('html').attr('data-bs-theme') === 'dark'
  }

  const setTheme = theme => {
    const isDark = theme === 'auto' 
      ? window.matchMedia('(prefers-color-scheme: dark)').matches 
      : theme === 'dark'
    $('html').attr('data-bs-theme', isDark ? 'dark' : 'light')
  }

  const showActiveTheme = (theme, focus = false) => {
    const $themeSwitcher = $('#bd-theme')
    if (!$themeSwitcher.length) return

    const $btnToActive = $(`[data-bs-theme-value="${theme}"]`)
    const cssOfActiveBtn = $btnToActive.find('i').first().attr('class')

    $('[data-bs-theme-value]').each(function() {
      $(this)
        .attr('aria-pressed', 'false')
        .removeClass('active')
        .find('i:nth-child(2)')
        .addClass('d-none')
    })

    $btnToActive
      .addClass('active')
      .attr('aria-pressed', 'true')
      .find('i:nth-child(2)')
      .removeClass('d-none')

    $('#bd-theme > i').attr('class', cssOfActiveBtn)
    const themeSwitcherLabel = `${$('#bd-theme-text').text()} (${theme})`
    $themeSwitcher.attr('aria-label', themeSwitcherLabel)

    if (focus) {
      $themeSwitcher.focus()
    }
  }

  // initialize theme
  setTheme(getPreferredTheme())

  // listen system theme change
  window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', () => {
    const storedTheme = getStoredTheme()
    if (storedTheme !== 'light' && storedTheme !== 'dark') {
      setTheme(getPreferredTheme())
    }
  })

  $(document).ready(() => {
    showActiveTheme(getPreferredTheme())

    $('[data-bs-theme-value]').on('click', function() {
      const theme = $(this).data('bs-theme-value')
      setStoredTheme(theme)
      setTheme(theme)
      showActiveTheme(theme, true)
      $('#navbar').collapse('hide')
    })
  })
})();

// wechat pay
(() => {
  'use strict'
  
  // unified processing of wechat payment
  function wxPay(params, callback) {
    const data = {
      amount: params.amount,
      businessId: params.businessId,
      businessType: params.businessType,
      payType: "wxpay",
      tradeType: params.openId ? "jsapi" : "native"
    };
    
    if (params.openId) {
      data.openId = params.openId;
    }

    $.ajax({
      url: EASTER_DOMAIN + 'api/pay/order',
      type: "post",
      dataType: "json",
      contentType: "application/json",
      data: JSON.stringify(data),
      success: ({content}) => {
        if (data.tradeType === "jsapi") {
          WeixinJSBridge.invoke('getBrandWCPayRequest', content.detail,
            res => callback(res.err_msg === "get_brand_wcpay_request:ok")
          );
        } else {
          callback(content.detail.code_url);
        }
      }
    });
  }

  let qrcode = null;
  $(function() {
    const $elements = {
      box: $('#wxpay-box'),
      qrcode: $('#wxpay-qrcode'),
      tips: $('#wxpay-tips'),
      amount: $('#wxpay-amount')
    };

    $('#wxpay-btn').on('click', () => {
      $elements.box.toggle();
      if ($elements.box.is(':visible')) {
        $elements.qrcode.hide();
        $elements.tips.hide();
      }
    });

    $('#wxpay-amount-group').on('click', 'button', 
      e => $elements.amount.val($(e.target).data('amount'))
    );

    $('#wxpay-submit').on('click', () => {
      const amount = $elements.amount.val();
      if (!amount) {
        return showToast('请输入赞赏金额');
      }

      const params = {
        amount: amount > 0 ? parseInt(amount * 100) : amount,
        businessType: PAY_BUSINESS_TYPE || 'donate',
        businessId: PAY_BUSINESS_ID
      };

      if (WX_OPEN_ID) {
        params.openId = WX_OPEN_ID;
        wxPay(params, success => {
          if (success) {
            $elements.box.hide();
            showToast('感谢支持，主佑平安🙏');
          }
        });
      } else {
        wxPay(params, url => {
          $elements.qrcode.show();
          $elements.tips.show();
          
          if (qrcode) {
            qrcode.clear();
            qrcode.makeCode(url);
          } else {
            qrcode = new QRCode('wxpay-qrcode', {
              text: url,
              width: 256,
              height: 256,
              colorDark: '#000000',
              colorLight: '#ffffff',
              correctLevel: QRCode.CorrectLevel.H
            });
          }
        });
      }
    });
  });
})();

// module navigation
(() => {
  'use strict'
  
  $(function() {
    const module = util.getUrlParam('m');
    if (module) {
      const $navItems = $('#navbar-links > li.nav-item');
      $navItems.removeClass('active');
      
      const $activeItem = $navItems.find(`a[href*="m=${module}"]`).parent();
      $activeItem.length ? $activeItem.addClass('active') : $navItems.last().addClass('active');
    }
  });
})();


// bible version
(() => {
  'use strict'
  
  $(function() {
    const $version = $('#bible-version');
    $version.on('change', () => {
      if(util.getUrlParam('version')) {
        window.location.href = window.location.href.replace(util.getUrlParam('version'), $version.val());
      } else {
        let url = location.href.replace(location.hash,"");
        window.location.href = url + '&version=' + $version.val();
      }
    });
  });
})();

// music player
(() => {
  'use strict'
  
  $(function() {
    $('.card-music').each(function(i, card){
      const trackId = $(card).attr('data-trackId');
      const albumId = $(card).attr('data-albumId');
      const singerId = $(card).attr('data-singerId');
      const mp3url = $(card).attr('data-mp3url');
      const thumbnail = $(card).attr('data-thumbnail');
      const trackName = $(card).attr('data-trackName');
      const albumName = $(card).attr('data-albumName');
      const singerName = $(card).attr('data-singerName');

      let link = $(card).find('a').first().attr('href');
      $(card).after(`<a class="fs-7" style="display:block; text-align:center;" href="${link}" target="_blank">点击查看：${trackName} - ${singerName}</a>`)
      const ap = new APlayer({
          container: card,
          preload: 'none',
          loop: 'none',
          audio: [{
              name: trackName,
              artist: singerName,
              url: mp3url,
              cover: thumbnail+"@!w100h100"
          }]
      });
      ap.on('play', function() {
          statistic.updateTrack(trackId);
      });
    });
  })
})();

// common method
(() => {
  'use strict'
  
  $(function() {
    //match night mode
    if(isDark()) {
      $(".article-content").find("span").each(function(i, item){
        item.style.backgroundColor = '';
        item.style.color = '';
      });
    }

    $("#top-guider button.btn-close").on('click', () => {
      $("#top-guider").addClass('d-none');
      util.setStorage('top-guider-closed', new Date().getTime());
    });

    // if 24 hours have not been closed, then show
    if(!util.getStorage('top-guider-closed') || util.getStorage('top-guider-closed') < (new Date().getTime() - 1000*60*60*24)) {
      $("#top-guider").removeClass('d-none');
    }

    util.updateWxShare();
  })
})();