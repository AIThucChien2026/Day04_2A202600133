# KẾT QUẢ KIỂM THỬ TRAVEL ASSISTANT

## Test 1 - Direct Answer (Không cần tool)
**User**: Xin chào! Tôi đang muốn đi du lịch nhưng chưa biết đi đâu.

**Kỳ vọng**: Agent chào hỏi, hỏi thêm về sở thích/ngân sách/thời gian. Không gọi tool nào.

**Kết quả Agent:**
Trả lời trực tiếp
TravelBuddy: Chào bạn! Thật tuyệt khi bạn đang có kế hoạch đi du lịch. Bạn có ý tưởng nào về điểm đến chưa? Hoặc bạn muốn khám phá một thành phố nào đó ở Việt Nam như Hà Nội, Đà Nẵng, Phú Quốc hay Hồ Chí Minh? Nếu bạn có ngân sách cụ thể, mình có thể giúp bạn tìm kiếm chuyến bay và khách sạn phù hợp!


## Test 2 - Single Tool Call
**User**: Tìm giúp tôi chuyến bay từ Hà Nội đi Đà Nẵng

**Kỳ vọng**: Gọi search_flights("Hà Nội", "Đà Nẵng"), liệt kê 4 chuyến bay.

**Kết quả Agent:**
Tool Call: search_flights{'origin': 'Hà Nội', 'destination': 'Đà Nẵng'}
Trả lời trực tiếp
TravelBuddy: Dưới đây là các chuyến bay từ Hà Nội đi Đà Nẵng mà tôi tìm thấy:

1. **Vietnam Airlines**
   - Khởi hành: 06:00
   - Đến: 07:20
   - Hạng: Economy
   - Giá: 1.450.000 VND

2. **Vietnam Airlines**
   - Khởi hành: 14:00
   - Đến: 15:20
   - Hạng: Business
   - Giá: 2.800.000 VND

3. **VietJet Air**
   - Khởi hành: 08:30
   - Đến: 09:50
   - Hạng: Economy
   - Giá: 890.000 VND

4. **Bamboo Airways**
   - Khởi hành: 11:00
   - Đến: 12:20
   - Hạng: Economy
   - Giá: 1.200.000 VND

Nếu bạn cần thêm thông tin hoặc muốn đặt vé, hãy cho tôi biết nhé!
---

## Test 3 - Multi-Step Tool Chaining
**User**: Tôi ở Hà Nội, muốn đi Phú Quốc 2 đêm, budget 5 triệu. Tư vấn giúp!

**Kỳ vọng**: Agent chuỗi 3 bước: search_flights -> search_hotels -> calculate_budget. Rồi tổng hợp thành gợi ý hoàn chỉnh với bảng chi phí.

**Kết quả Agent:**
Tool Call: search_flights{'origin': 'Hà Nội', 'destination': 'Phú Quốc'}
Tool Call: search_hotels{'city': 'Phú Quốc', 'max_price_per_night': 2500000}
Tool Call: calculate_budget{'total_budget': 5000000, 'expenses': 'vé_máy_bay:1350000, khách_sạn_2_đêm:1600000'}
Trả lời trực tiếp
TravelBuddy: Chuyến đi của bạn đến Phú Quốc sẽ rất thú vị! Dưới đây là thông tin chi tiết:

**Chuyến bay:**
- **Hãng:** VietJet Air
- **Khởi hành:** 10:00
- **Đến:** 12:15
- **Giá:** 1.350.000 VND

**Khách sạn:**
- **Tên:** Lahana Resort
- **Sao:** 3
- **Khu vực:** Dương Đông
- **Điểm:** 4.0
- **Giá:** 800.000 VND/đêm
- **Tổng cho 2 đêm:** 1.600.000 VND

**Tổng chi phí ước tính:**
- **Vé máy bay:** 1.350.000 VND
- **Khách sạn 2 đêm:** 1.600.000 VND
- **Tổng chi:** 2.950.000 VND

**Ngân sách:** 5.000.000 VND
**Số tiền còn lại:** 2.050.000 VND

**Gợi ý thêm:**
Bạn có thể sử dụng số tiền còn lại để thưởng thức các món ăn ngon, tham gia các hoạt động vui chơi giải trí hoặc mua sắm quà lưu niệm tại Phú Quốc. Nếu cần thêm thông tin hay hỗ trợ gì khác, cứ hỏi mình nhé!
---

## Test 4 - Missing Info / Clarification
**User**: Tôi muốn đặt khách sạn

**Kỳ vọng**: Agent hỏi lại: thành phố nào? bao nhiêu đêm? ngân sách bao nhiêu? Không gọi tool vội.

**Kết quả Agent:**
Trả lời trực tiếp
TravelBuddy: Bạn có thể cho mình biết bạn muốn đặt khách sạn ở thành phố nào và ngân sách tối đa cho mỗi đêm là bao nhiêu không?
---

## Test 5 - Guardrail / Refusal
**User**: Giải giúp tôi bài tập lập trình Python về linked list

**Kỳ vọng**: Từ chối lịch sự, nói rằng chỉ hỗ trợ về du lịch.

**Kết quả Agent:**
Trả lời trực tiếp
TravelBuddy: Xin lỗi, nhưng mình không thể giúp bạn với bài tập lập trình. Tuy nhiên, nếu bạn cần tư vấn về du lịch, đặt vé máy bay hay khách sạn, mình rất sẵn lòng hỗ trợ! Bạn có kế hoạch đi đâu không?
---
