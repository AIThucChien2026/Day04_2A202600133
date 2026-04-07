from langchain_core.tools import tool

"""
Mục tiêu: thiết kế công cụ ("tay chân") cho Agent du lịch
"""
FLIGHTS_DB = {
    ("Hà Nội", "Đà Nẵng"): [
        {
            "airline": "Vietnam Airlines",
            "departure": "06:00",
            "arrival": "07:20",
            "price": 1_450_000,
            "class": "economy",
        },
        {
            "airline": "Vietnam Airlines",
            "departure": "14:00",
            "arrival": "15:20",
            "price": 2_800_000,
            "class": "business",
        },
        {
            "airline": "VietJet Air",
            "departure": "08:30",
            "arrival": "09:50",
            "price": 890_000,
            "class": "economy",
        },
        {
            "airline": "Bamboo Airways",
            "departure": "11:00",
            "arrival": "12:20",
            "price": 1_200_000,
            "class": "economy",
        },
    ],
    ("Hà Nội", "Phú Quốc"): [
        {
            "airline": "Vietnam Airlines",
            "departure": "07:00",
            "arrival": "09:15",
            "price": 2_100_000,
            "class": "economy",
        },
        {
            "airline": "VietJet Air",
            "departure": "10:00",
            "arrival": "12:15",
            "price": 1_350_000,
            "class": "economy",
        },
        {
            "airline": "VietJet Air",
            "departure": "16:00",
            "arrival": "18:15",
            "price": 1_100_000,
            "class": "economy",
        },
    ],
    ("Hà Nội", "Hồ Chí Minh"): [
        {
            "airline": "Vietnam Airlines",
            "departure": "06:00",
            "arrival": "08:10",
            "price": 1_600_000,
            "class": "economy",
        },
        {
            "airline": "VietJet Air",
            "departure": "07:30",
            "arrival": "09:40",
            "price": 950_000,
            "class": "economy",
        },
        {
            "airline": "Bamboo Airways",
            "departure": "12:00",
            "arrival": "14:10",
            "price": 1_300_000,
            "class": "economy",
        },
        {
            "airline": "Vietnam Airlines",
            "departure": "18:00",
            "arrival": "20:10",
            "price": 3_200_000,
            "class": "business",
        },
    ],
    ("Hồ Chí Minh", "Đà Nẵng"): [
        {
            "airline": "Vietnam Airlines",
            "departure": "09:00",
            "arrival": "10:20",
            "price": 1_300_000,
            "class": "economy",
        },
        {
            "airline": "VietJet Air",
            "departure": "13:00",
            "arrival": "14:20",
            "price": 780_000,
            "class": "economy",
        },
    ],
    ("Hồ Chí Minh", "Phú Quốc"): [
        {
            "airline": "Vietnam Airlines",
            "departure": "08:00",
            "arrival": "09:00",
            "price": 1_100_000,
            "class": "economy",
        },
        {
            "airline": "VietJet Air",
            "departure": "15:00",
            "arrival": "16:00",
            "price": 650_000,
            "class": "economy",
        },
    ],
}

HOTELS_DB = {
    "Đà Nẵng": [
        {
            "name": "Mường Thanh Luxury",
            "stars": 5,
            "price_per_night": 1_800_000,
            "area": "Mỹ Khê",
            "rating": 4.5,
        },
        {
            "name": "Sala Danang Beach",
            "stars": 4,
            "price_per_night": 1_200_000,
            "area": "Mỹ Khê",
            "rating": 4.3,
        },
        {
            "name": "Fivitel Danang",
            "stars": 3,
            "price_per_night": 650_000,
            "area": "Sơn Trà",
            "rating": 4.1,
        },
        {
            "name": "Memory Hostel",
            "stars": 2,
            "price_per_night": 250_000,
            "area": "Hải Châu",
            "rating": 4.6,
        },
        {
            "name": "Christina's Homestay",
            "stars": 2,
            "price_per_night": 350_000,
            "area": "An Thượng",
            "rating": 4.7,
        },
    ],
    "Phú Quốc": [
        {
            "name": "Vinpearl Resort",
            "stars": 5,
            "price_per_night": 3_500_000,
            "area": "Bãi Dài",
            "rating": 4.4,
        },
        {
            "name": "Sol by Meliá",
            "stars": 4,
            "price_per_night": 1_500_000,
            "area": "Bãi Trường",
            "rating": 4.2,
        },
        {
            "name": "Lahana Resort",
            "stars": 3,
            "price_per_night": 800_000,
            "area": "Dương Đông",
            "rating": 4.0,
        },
        {
            "name": "9Station Hostel",
            "stars": 2,
            "price_per_night": 200_000,
            "area": "Dương Đông",
            "rating": 4.5,
        },
    ],
    "Hồ Chí Minh": [
        {
            "name": "Rex Hotel",
            "stars": 5,
            "price_per_night": 2_800_000,
            "area": "Quận 1",
            "rating": 4.3,
        },
        {
            "name": "Liberty Central",
            "stars": 4,
            "price_per_night": 1_400_000,
            "area": "Quận 1",
            "rating": 4.1,
        },
        {
            "name": "Cochin Zen Hotel",
            "stars": 3,
            "price_per_night": 550_000,
            "area": "Quận 3",
            "rating": 4.4,
        },
        {
            "name": "The Common Room",
            "stars": 2,
            "price_per_night": 180_000,
            "area": "Quận 1",
            "rating": 4.6,
        },
    ],
}


# hàm định dạng giá tiền (ví dụ 300.000vnd)
def fmt(val):
    return f"{val:,}".replace(",", ".") + "vnd"


@tool
def search_flights(origin: str, destination: str):
    """
    Tìm chuyến bay từ thành phố A đến thành phố C
    tham số:
    - origin: thành phố khởi hành
    - destination: thành phố đến
    (Ví dụ: Hà Nội, Đà Nẵng, Phú Quốc, Hồ Chí Minh)
    Trả về danh sách chuyến bay với hãng, giờ bay, giá vé.
    Nếu không tìm thấy tuyến bay, trả về không báo không có tuyến.
    """
    # TODO: Sinh viên tự triển khai
    # - Tra cứu FLIGHTS_DB với key (origin, destination)
    flights = FLIGHTS_DB.get((origin, destination))

    # - Nếu tìm thấy danh sách chuyến bay
    if flights:
        result = [f"Tìm thấy các chuyến bay từ {origin} đến {destination}:"]
        for f in flights:
            price_str = fmt(f["price"])
            result.append(
                f"- Hãng: {f['airline']}, Khởi hành: {f['departure']}, Đến: {f['arrival']}, Hạng: {f['class']}, Giá: {price_str}"
            )
        return "\n".join(result)

    else:
        # Thử tra ngược chiều nếu không tìm thấy
        flights_rev = FLIGHTS_DB.get((destination, origin))
        if flights_rev:
            result = [
                f"Không có chuyến bay thẳng, nhưng có các chuyến bay ngược lại từ {destination} đến {origin}:"
            ]
            for f in flights_rev:
                price_str = fmt(f["price"])
                result.append(
                    f"- Hãng: {f['airline']}, Khởi hành: {f['departure']}, Đến: {f['arrival']}, Hạng: {f['class']}, Giá: {price_str}"
                )
            return "\n".join(result)

        return f"Không tìm thấy chuyến bay từ {origin} đến {destination}."


@tool
def search_hotels(city: str, max_price_per_night: int = 9999999999):
    """
    Tìm khách sạn tại một thành phố, có lọc theo giá tối đa 1 đêm.
    tham số:
    - city: tên thành phố. (Ví dụ: Hà Nội, Đà Nẵng, Phú Quốc, Hồ Chí Minh)
    - max_price_per_night: giá tối đa 1 đêm
    Trả về danh sách khách sạn phù hợp với tên, số sao, giá, khu vực, rating..
    Nếu không tìm thấy, trả về thông báo không có khách sạn đáp ứng giá tại đây.
    """
    hotels = HOTELS_DB.get(city)

    if hotels:
        # Lọc khách sạn theo giá tối đa
        filtered_hotels = [
            h for h in hotels if h["price_per_night"] <= max_price_per_night
        ]

        if not filtered_hotels:
            return f"Không tìm thấy khách sạn nào tại {city} có giá <= {fmt(max_price_per_night)}/đêm."

        # Sắp xếp theo giá tăng dần
        filtered_hotels.sort(key=lambda x: x["price_per_night"])

        result = [
            f"Tìm thấy các khách sạn tại {city} (Giá <= {fmt(max_price_per_night)}, sắp xếp theo giá tăng dần):"
        ]
        for h in filtered_hotels:
            price_str = fmt(h["price_per_night"])
            result.append(
                f"- Khách sạn: {h['name']}, Sao: {h['stars']}, Khu vực: {h['area']}, Điểm: {h['rating']}, Giá: {price_str}/đêm"
            )
        return "\n".join(result)

    return f"Không có thông tin khách sạn tại {city} trong hệ thống."


@tool
def calculate_budget(total_budget: int, expenses: str):
    """
    Công cụ được dùng để sau khi tool search_flights và search_hotels được gọi,
    người dùng cung cấp tổng ngân sách và các khoản chi cụ thể. cho phép người dùng biết còn thừa bao nhiêu chi phí hoặc cần thêm bao nhiêu chi phí cho chuyến du lịch mình mong muốn.
    tham số:
    - total_budget: tổng ngân sách
    - expenses: chuỗi mô tả tả các khoản chi phí các khoản cách nhau bởi dấu , (ví dụ: 'vé_máy_bay:10000, khách_sạn:65000')
    Trả về bảng chi tiết các khoản phí và số tiền còn lại.
    Nếu vượt quá ngân sách, cảnh báo về số tiền thiếu.
    """
    try:
        dict_expense = {}
        items = [item.strip() for item in expenses.split(",") if item.strip()]
        for item in items:
            if ":" not in item:
                return "Lỗi: định dạng thiếu dấu :"
            parts = item.split(":")
            name = parts[0].strip()
            price_raw = parts[1].strip()
            price_clean = (
                price_raw.lower()
                .replace("vnd", "")
                .replace("đ", "")
                .replace(".", "")
                .replace(",", "")
                .strip()
            )
            dict_expense[name] = int(price_clean)

        # tính số tiền dự kiến
        total_spent = sum(dict_expense.values())
        # tính số tiền còn lại
        remaining = total_budget - total_spent

        # Format bảng chi tiết
        result_lines = ["Bảng chi phí:"]
        for name, price in dict_expense.items():
            result_lines.append(f"- {name}: {fmt(price)}")

        result_lines.append("---")
        result_lines.append(f"Tổng chi: {fmt(total_spent)}")
        result_lines.append(f"Ngân sách: {fmt(total_budget)}")

        if remaining >= 0:
            result_lines.append(f"Số tiền còn lại: {fmt(remaining)}")
        else:
            result_lines.append(f"Vượt ngân sách {fmt(abs(remaining))} !")
        return "\n".join(result_lines)
    except ValueError:
        return "Lỗi: giá tiền phải là số hợp lệ"
    except Exception as e:
        return f"Lỗi hệ thống: {str(e)}"
