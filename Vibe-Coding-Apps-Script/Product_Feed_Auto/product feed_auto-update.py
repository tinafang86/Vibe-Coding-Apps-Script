/**
 * =============================================================
 * ★★ 網站爬蟲 CONFIG 區塊 ★★
 * 針對 mall.sfworldwide.com 網站進行爬蟲設定
 * =============================================================
 */
const SFWORLDWIDE_CONFIG = {
  SPREADSHEET_ID:    '1uqJJ1L2Hy16m2IaOxa6OvOMJdUeRG2lYIEEfsCzh7D4',
  SHEET_NAME:        'sfworldwide_feed',
  BASE_URL:          'https://mall.sfworldwide.com', // 網站基礎網域
  COLLECTION_PATH:   '/categories/supplement',      // 產品列表頁的路徑
  PRODUCT_PATH_FILTER: '/supplement',       // 只抓取包含此路徑的產品

  RECIPIENT_EMAIL:   'tinafung8686@gmail.com',
  PROPERTY_KEY:      'sfworldwide_last_fetched_products',
  BRAND_NAME:        '佳格康研家'
};

/**
 * =============================================================
 * 主程式
 * =============================================================
 */
function updatesfworldwide () {
  const sheet = openSheet_(SFWORLDWIDE_CONFIG.SPREADSHEET_ID, SFWORLDWIDE_CONFIG.SHEET_NAME);
  
  // 1. 抓取所有產品列表上的初步資料
  const allProducts = fetchAllProducts_(SFWORLDWIDE_CONFIG.BASE_URL, SFWORLDWIDE_CONFIG.COLLECTION_PATH);
  
  // 2. 過濾產品：只保留網址包含特定路徑的產品
  const newProducts = allProducts.filter(p => p.productLink.includes(SFWORLDWIDE_CONFIG.PRODUCT_PATH_FILTER));
  Logger.log(`篩選後，符合 '${SFWORLDWIDE_CONFIG.PRODUCT_PATH_FILTER}' 路徑的產品共 ${newProducts.length} 筆。`);

  // 3. 讀取舊的產品資料以便比較
  const oldProducts = getOldProductsData_(SFWORLDWIDE_CONFIG.PROPERTY_KEY);
  
  // 4. 遍歷新產品，並為每個產品抓取詳細描述 (需要額外 HTTP 請求)
  for (let i = 0; i < newProducts.length; i++) {
    const product = newProducts[i];
    if (product.productLink) {
      Logger.log(`正在抓取產品 "${product.title}" 的描述...`);
      const description = fetchProductDescription_(product.productLink);
      product.description = description; // 更新產品物件的描述
    }
  }

  // 5. 將產品資料轉換為試算表行格式
  const newRows = newProducts.map(p => productToRow_(p, SFWORLDWIDE_CONFIG.BASE_URL, SFWORLDWIDE_CONFIG.BRAND_NAME));

  // 6. 清空試算表並寫入新的標題列和產品資料
  sheet.clearContents();
  sheet.appendRow([
    'id','title','description','availability',
    'condition','price','link','image_link','brand'
  ]);
  if (newRows.length) {
    sheet.getRange(2, 1, newRows.length, newRows[0].length).setValues(newRows);
  }

  // 7. 比較新舊資料差異並發送 Email 通知
  compareAndNotify_(
    oldProducts, newProducts,
    SFWORLDWIDE_CONFIG.BASE_URL, SFWORLDWIDE_CONFIG.COLLECTION_PATH,
    SFWORLDWIDE_CONFIG.RECIPIENT_EMAIL,
    SFWORLDWIDE_CONFIG.BRAND_NAME
  );

  // 8. 儲存當前產品資料作為下一次比較的舊資料
  saveCurrentProductsData_(newProducts, SFWORLDWIDE_CONFIG.PROPERTY_KEY);
}

/**
 * =============================================================
 * ↓↓↓               輔助工具函式 (Helper Functions)            ↓↓↓
 * =============================================================
 */

/**
 * 開啟或建立 Google 試算表中的特定工作表
 * @param {string} spreadsheetId 試算表的 ID
 * @param {string} sheetName 工作表的名稱
 * @returns {GoogleAppsScript.Spreadsheet.Sheet} 工作表物件
 */
function openSheet_ (spreadsheetId, sheetName) {
  const ss = SpreadsheetApp.openById(spreadsheetId);
  let sh   = ss.getSheetByName(sheetName);
  if (!sh) sh = ss.insertSheet(sheetName);
  return sh;
}

/**
 * 從產品列表頁面解析產品資訊
 * @param {string} baseUrl 網站的基礎 URL
 * @param {string} collectionPath 產品列表頁的路徑
 * @returns {Array<Object>} 抓取到的產品資料陣列，每個物件包含 id, title, price, imageUrl, productLink 等
 */
function fetchAllProducts_ (baseUrl, collectionPath) {
  const products = [];
  const url = `${baseUrl}${collectionPath}`; // 構建產品列表頁的完整 URL
  Logger.log(`正在抓取產品列表頁: ${url}`);

  try {
    const response = UrlFetchApp.fetch(url, {muteHttpExceptions: true});
    if (response.getResponseCode() !== 200) {
      Logger.log(`Warning: Failed to fetch collection page from ${url}. Status Code: ${response.getResponseCode()}`);
      return products; // 返回空陣列
    }

    const htmlContent = response.getContentText();

    // 根據你提供的 HTML 片段，最外層的產品包裹是一個 class="quick-cart-item" 的 <a> 標籤
    const productBlocks = htmlContent.match(/<a[^>]*class="quick-cart-item[^>]*>[\s\S]*?<\/a>/g);

    if (!productBlocks || productBlocks.length === 0) {
      Logger.log('沒有找到產品區塊 (quick-cart-item)，請檢查 Regex 或頁面結構。');
      return products;
    }
    
    Logger.log(`找到 ${productBlocks.length} 個產品區塊 (初步)。`);

    productBlocks.forEach((block, index) => {
      // 1. 產品連結 (href)
      const linkMatch = block.match(/href="([^"]+)"/);
      const productLink = linkMatch && linkMatch[1] ? normalizeHttps_(linkMatch[1].trim()) : '';

      // 2. 產品圖片 (data-srcset) - 抓取第一個 srcset URL
      const imageMatch = block.match(/<img[^>]*data-srcset="([^"]+)"/);
      let imageUrl = '';
      if (imageMatch && imageMatch[1]) {
        // 從 srcset 字串中提取第一個圖片 URL
        const srcsetParts = imageMatch[1].split(',').map(s => s.trim());
        if (srcsetParts.length > 0) {
          imageUrl = normalizeHttps_(srcsetParts[0].split(' ')[0]); // 取第一個URL
        }
      }

      // 3. 產品標題 (div class="title")
      const titleMatch = block.match(/<div class="title[^>]*>([\s\S]*?)<\/div>/);
      const productTitle = titleMatch && titleMatch[1] ? cleanHtmlText_(titleMatch[1].trim()) : '';

      // 4. 產品價格 (div class="price-sale")
      const priceMatch = block.match(/<div class="price-sale[^>]*>\s*NT\$([\d,.]+)/);
      const productPrice = priceMatch && priceMatch[1] ? parseFloat(priceMatch[1].replace(/,/g, '')) : 0;

      // 5. 產品 ID (_id 屬性在 ga-product 的 JSON 內)
      const gaProductMatch = block.match(/ga-product="({[^}]+})"/);
      let productId = `P${index + 1}`; // 預設一個臨時 ID
      if (gaProductMatch && gaProductMatch[1]) {
        try {
          const jsonString = gaProductMatch[1].replace(/&quot;/g, '"'); // 轉換 HTML 實體
          const gaProductData = JSON.parse(jsonString);
          if (gaProductData && gaProductData.id) { // 注意這裡從 _id 改為 id，因為 Shopline 的 ga-product 裡通常是 "id"
            productId = gaProductData.id;
          } else if (gaProductData && gaProductData._id) { // 兼容 _id
            productId = gaProductData._id;
          }
        } catch (e) {
          Logger.log(`解析 ga-product JSON 失敗 (區塊 ${index}): ${e.message}`);
        }
      }

      // 確保所有關鍵資訊都成功獲取，才加入列表
      if (productLink && imageUrl && productTitle && productPrice > 0) {
        const product = {
          id: productId,
          title: productTitle,
          productLink: productLink,
          imageUrl: imageUrl,
          price: productPrice,
          description: '', // 描述會稍後單獨抓取
          available: true // 暫時為 true
        };
        products.push(product);
      } else {
        Logger.log(`未能完全解析產品區塊 ${index} 的部分資訊，已跳過。` +
                   `Title: "${productTitle || 'N/A'}", ` +
                   `Link: "${productLink || 'N/A'}", ` +
                   `Image: "${imageUrl || 'N/A'}", ` +
                   `Price: "${productPrice || 'N/A'}"`);
      }
    });

  } catch (e) {
    Logger.log(`🚨 抓取產品列表時發生錯誤: ${e.message}`);
  }
  return products;
}

/**
 * 從產品詳情頁抓取 meta description
 * @param {string} productUrl 產品詳情頁的 URL
 * @returns {string} 抓取到的 meta description 內容，如果失敗則返回空字串
 */
function fetchProductDescription_ (productUrl) {
  try {
    const response = UrlFetchApp.fetch(productUrl, {muteHttpExceptions: true, followRedirects: true});
    if (response.getResponseCode() !== 200) {
      Logger.log(`Warning: Failed to fetch product page for description from ${productUrl}. Status Code: ${response.getResponseCode()}`);
      return '';
    }
    const htmlContent = response.getContentText();
    // 強化正規表達式，使其更具彈性，例如處理單引號、多個空白等
    const match = htmlContent.match(/<meta\s+name="description"\s+content="([^"]*)"[^>]*>/i); // 忽略大小寫
    const description = match && match[1] ? match[1].trim() : '';
    
    if (!description) {
      Logger.log(`未能從 ${productUrl} 抓取到 meta description。`);
    }
    return description;

  } catch (e) {
    Logger.log(`🚨 抓取產品描述時發生錯誤於 ${productUrl}: ${e.message}`);
    return '';
  }
}

/**
 * 將產品物件轉換為 Google 試算表所需的一行資料格式
 * @param {Object} product 從網頁爬取到的產品物件
 * @param {string} baseUrl 網站基礎 URL
 * @param {string} brandName 品牌名稱
 * @returns {Array<string>} 試算表的一行資料
 */
function productToRow_ (product, baseUrl, brandName) {
  const productId = product.id;
  const productTitle = product.title;
  // description 已經在 updateMaterna 函數中被填充
  const productDescription = product.description || '無描述'; 
  const productAvailability = product.available ? 'in stock' : 'out of stock';
  const productCondition = 'new';
  const priceStr = product.price ? `${product.price} TWD` : '0 TWD';
  const productLink = product.productLink;
  const imageUrl = product.imageUrl;
  
  return [
    productId,
    productTitle,
    productDescription,
    productAvailability,
    productCondition,
    priceStr,
    productLink,
    imageUrl,
    brandName
  ];
}

/**
 * 清理從 HTML 元素中提取的文本，移除 HTML 標籤並限制長度
 * @param {string} html 包含 HTML 標籤的原始文本
 * @returns {string} 清理後的純文本
 */
function cleanHtmlText_(html) {
  if (!html) return '';
  let cleanedText = html.replace(/<[^>]*>/g, '');
  cleanedText = cleanedText.replace(/\s+/g, ' ').trim();
  const MAX_DESCRIPTION_LENGTH = 500;
  if (cleanedText.length > MAX_DESCRIPTION_LENGTH) {
    cleanedText = cleanedText.substring(0, MAX_DESCRIPTION_LENGTH) + '...';
  }
  return cleanedText;
}

/**
 * 正規化 URL，確保是完整的 HTTPS 連結
 * @param {string} url 原始 URL
 * @returns {string} 正規化後的 HTTPS URL
 */
function normalizeHttps_ (url) {
  if (!url) return '';
  // 檢查是否已經是完整 HTTPS URL
  if (url.startsWith('https://')) return url;
  if (url.startsWith('http://')) return 'https://' + url.slice(7); // 將 HTTP 轉換為 HTTPS
  // 對於相對路徑（如 /products/...），需要加上 baseUrl
  if (url.startsWith('/')) return `${SFWORLDWIDE_CONFIG.BASE_URL}${url}`;
  // 如果是 Shopline 的 CDN 網址，它們通常是 // 開頭，自動補上 https:
  if (url.startsWith('//')) return 'https:' + url;
  
  return url; // 如果都不是上述情況，直接返回原 URL
}

/**
 * 從 Apps Script 屬性服務中讀取舊的產品資料
 * @param {string} propertyKey 儲存資料的鍵名
 * @returns {Object} 舊的產品資料物件 (ID:Title Map)
 */
function getOldProductsData_(propertyKey) {
  const properties = PropertiesService.getScriptProperties();
  const jsonString = properties.getProperty(propertyKey);
  return jsonString ? JSON.parse(jsonString) : {};
}

/**
 * 將當前產品資料儲存到 Apps Script 屬性服務中，用於下次比較
 * @param {Array<Object>} products 當前抓取到的產品資料陣列
 * @param {string} propertyKey 儲存資料的鍵名
 */
function saveCurrentProductsData_(products, propertyKey) {
  const productMap = products.reduce((acc, p) => {
    acc[p.id] = p.title;
    return acc;
  }, {});
  PropertiesService.getScriptProperties().setProperty(propertyKey, JSON.stringify(productMap));
}

/**
 * 比較新舊產品資料，並發送 Email 通知產品變動
 * @param {Object} oldData 舊的產品資料 (ID:Title Map)
 * @param {Array<Object>} newData 新的產品資料陣列
 * @param {string} shopDomainOrBaseUrl 商店網域或基礎 URL
 * @param {string} collectionHandleOrPath 產品列表路徑
 * @param {string} recipientEmail 收件人 Email
 * @param {string} brandName 品牌名稱
 */
function compareAndNotify_(
  oldData, newData,
  shopDomainOrBaseUrl, collectionHandleOrPath,
  recipientEmail,
  brandName
) {
  const newProductIds = new Set(newData.map(p => p.id));
  const removedProducts = [];
  const addedProducts = [];

  for (const id in oldData) {
    if (!newProductIds.has(id)) { // 確保 ID 類型一致，這裡應為字串比對
      removedProducts.push(oldData[id]);
    }
  }

  for (const p of newData) {
    if (!oldData[p.id]) {
      addedProducts.push(p.title);
    }
  }

  const now = new Date();
  const dateTimeOptions = {
    year: 'numeric', month: '2-digit', day: '2-digit',
    hour: '2-digit', minute: '2-digit', second: '2-digit',
    hour12: false, timeZone: 'Asia/Taipei'
  };
  const dateTimeStr = now.toLocaleString('zh-TW', dateTimeOptions);

  const dateOnlyStr = now.toLocaleString('zh-TW', {
    year: 'numeric', month: '2-digit', day: '2-digit', timeZone: 'Asia/Taipei'
  }).replace(/\//g, '-');

  // --- 構建 Email 內容 ---
  let subject = `【產品更新通知】${brandName} ${dateOnlyStr}`;
  let emailBody = `產品檢查時間：${dateTimeStr} (台灣時間)\n\n`;

  let hasChanges = false;
  if (removedProducts.length === 0 && addedProducts.length === 0) {
    emailBody += '--- 無產品變動 ---\n\n試算表產品資料已確認為最新。\n';
  } else {
    hasChanges = true;
    emailBody += '--- 產品變動摘要 ---\n';
    if (addedProducts.length) {
      emailBody += `- 新增產品：${addedProducts.length} 筆\n`;
    }
    if (removedProducts.length) {
      emailBody += `- 下架產品：${removedProducts.length} 筆\n`;
    }
    emailBody += '\n';

    if (removedProducts.length) {
      emailBody += '--- 已下架產品清單 ---\n';
      removedProducts.forEach(t => emailBody += `- ${t}\n`);
      emailBody += '\n';
    }
    if (addedProducts.length) {
      emailBody += '--- 新上架產品清單 ---\n';
      addedProducts.forEach(t => emailBody += `- ${t}\n`);
      emailBody += '\n';
    }
    subject += ' (有變動)'; // 如果有變動，主旨加上標記
  }

  const oldTitles = Object.values(oldData);
  if (oldTitles.length) {
    emailBody += `--- 更新前產品清單 (${oldTitles.length} 筆) ---\n`;
    oldTitles.forEach(t => emailBody += `- ${t}\n`);
    emailBody += '\n';
  }

  const newTitles = newData.map(p => p.title);
  if (newTitles.length) {
    emailBody += `--- 更新後產品清單 (${newTitles.length} 筆) ---\n`;
    newTitles.forEach(t => emailBody += `- ${t}\n`);
    emailBody += '\n';
  }
  
  // 加入試算表連結
  emailBody += `查看試算表：https://docs.google.com/spreadsheets/d/${SFWORLDWIDE_CONFIG.SPREADSHEET_ID}/edit\n`;
  // 加入產品列表連結
  emailBody += `前往產品列表頁：${shopDomainOrBaseUrl}${collectionHandleOrPath}\n`;


  // 這裡明確使用 GmailApp.sendEmail 發送郵件
  GmailApp.sendEmail(recipientEmail, subject, emailBody);
  Logger.log('📩 產品更新郵件已發送。');
}